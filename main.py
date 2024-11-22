from fasthtml.common import *
import numpy as np
import matplotlib.colors as mcolors
import uuid_utils as uuid
import ast
import asyncio
from colormaps import get_random_discrete_colors
import os

os.environ['MPLCONFIGDIR'] = '/tmp'

from data import *
# from plot_section import *
# from color_section import *
from styling import *

# Database for storing plot and color configurations
tables = database('conf.db').t
conf = tables.conf
if not conf in tables:
    conf.create(session_id=str,
                plot_type=str,
                nr_points=int,
                alpha=float,
                data_type=str,
                size_scatter=int,
                marker=str,
                line_thickness=int,
                noise=float,
                markersize=int,
                nr_colors=int,
                color_list=str,
                color_data_type=str,
                test_color=str,
                show_splines=bool,
                show_outlines=bool,
                nr_bins=int,
                offset=int,
                seed=int,
                pk='session_id')
Conf = conf.dataclass()


def add_session(session_id):
    global conf
    # session_conf[session_id] = conf_plot
    new_conf = conf.insert(Conf(session_id=session_id, **conf_plot))


def queryDB(session_id):
    print("Session_id: ", session_id)
    try:
        # print("Lookup: ", conf.lookup(lookup_values = {"session_id": session_id}))
        # return conf.lookup(lookup_values = {"session_id": session_id})
        return conf.get(session_id)
    except Exception as e:
        print("Exception: ", e)
        return None
    # return conf.get(session_id)


async def update_db(d: dict):
    global conf
    _ = conf.update(Conf(**d))


# GLOBAL VARIABLES
conf_plot = {}

# BASE CONFIGURATION
conf_plot['plot_type'] = 'scatter'
conf_plot['data_type'] = 'discrete'
conf_plot['nr_points'] = 100
conf_plot['alpha'] = 1
conf_plot['size_scatter'] = 5
conf_plot['marker'] = 'o'
conf_plot['line_thickness'] = 1
conf_plot['noise'] = 0.5
conf_plot['markersize'] = 4
conf_plot['nr_colors'] = 3
conf_plot['color_list'] = "['#FFA500', '#FFC901', '#FFF000']"
conf_plot['color_data_type'] = "rgb"
conf_plot['test_color'] = '#FFF000'
conf_plot['show_splines'] = False
conf_plot['show_outlines'] = False
conf_plot['nr_bins'] = 10
conf_plot['offset'] = 1
conf_plot['seed'] = 1


def cst_slider():
    return Input


app, rt = fast_app(
    #secret_key = secret_key=os.getenv('SESSKEY', 's3kret')
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='css/pico.min.css', type='text/css'),
        Link(rel='stylesheet', href='css/custom.css', type='text/css'),
        # Link(rel='stylesheet',
        #      href='https://unpkg.com/normalize.css',
        #      type='text/css'),
        # picolink,  ## uncomment to get dark mode
        MarkdownJS(),
        HighlightJS(),
        css))


@rt("/")
def home(session):
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    # TODO: Check if session_id exists in the database
    try:
        add_session(session['session_id'])
    except:
        pass

    session_id = session['session_id']
    html = [
        Title("PyCMAP"),
        Favicon("matplotlib.ico",
                "matplotlib.ico"),  # Added to render Pico symbold on Website
        Div(
            Div(
                Img(src="icons/Matplotlib_icon.svg.png",
                    width="50px",
                    height="50px",
                    style="margin-right : 20px"),
                Titled("PyCMAP", style="height: 50px;"),
                # Button("Info",
                #        cls='cst_button',
                #        hx_get="info_page",
                #        hx_target="#page_content"),
                A("Buy me a Coffee",
                  cls='cst_button',
                  href="https://buymeacoffee.com/fabianjaeger"),
                style=
                'display: flex; align-items: center; justify-content: center; margin: 10px; padding-left: 20px; border-radius: 20px;'
            ),
            Div("Change colors and configure your plot to see your matplotlib colormap in realtime.",
                style=
                "color: grey; font-size: 18px; margin: 10px; padding-left: 20px; border-radius: 20px; margin-bottom: 30px;"
                ),
            Div(
                (show_color_selector(session_id), show_plots(session_id)),
                # style=parent_section,
                cls='parent_section'),
            # Footer(
            #     "Made by Fabian & Mila",
            #     style=
            #     'position: fixed; width: 100%; text-align: center; bottom: 0; left: 0; background-color: var(--pico-background-color); height:: 50px;'
            # ),
            id="page_content")
    ]
    return html


# TODO Implement the info page switch/popover

discrete_plot_types = ['Histogram', 'Plot', 'Scatter']
continous_plot_types = ["Density", "Heatmap"]


def color_presets(session_id: str):

    return Button(
        "Randomize Colors",
        # cls='cst_button',
        cls='background-color-pico-code',
        hx_target='#color_section',  #TODO Change to the correct parent container
        style=cst_button_style,
        hx_swap='outerHTML',
        hx_post='/change_color_preset',
        hx_vals={'session_id': session_id})


@app.post("/change_color_preset")
def change_color_preset(session_id: str):
    global conf
    plot_conf = queryDB(session_id)
    color_list = ast.literal_eval(plot_conf.color_list)
    nr_colors = len(color_list)

    color_list, cmap_name = get_random_discrete_colors(n_colors=nr_colors)

    # Update database with new colors
    plot_conf = queryDB(session_id)
    plot_conf.color_list = color_list  # Store as string representation
    # Add your database update logic here
    asyncio.run(
        update_db({
            "session_id": session_id,
            "color_list": plot_conf.color_list
        }))

    print(f"Session_id: {session_id}")
    print(f"COLOR LIST RAW: {color_list}")

    return show_color_selector(session_id)


def show_color_selector(session_id: str):
    # print("Session_id: {}".format(session_id))
    heading, color_grid, add = color_selector_raw(session_id)
    return Div(heading,
               color_presets(session_id),
               Div(color_grid,
                   cls='background-color-pico-code',
                   style=color_picker),
               cls='background-color-pico-code',
               id='color_section',
               style=grid_section)


def get_plot_footer(session_id):
    return Div(
        Div(
            Form(
                Select(
                    Option("Hex", value='hex'),
                    Option("RGB", value='rgb', default=True),
                    cls='cst_button',
                ),
                hx_post="/change_color_data_type",
                hx_target="#test",
                hx_vals={"session_id": session_id},
                style='margin-right: 5px;'  # Reduced margin
            ),
            Button("Get Code",
                   cls='cst_button',
                   hx_target="#code",
                   hx_swap='innerHTML',
                   hx_vals={"session_id": session_id},
                   get=return_code),
            style=
            'display: flex; flex-direction: row; align-items: center; justify-content: flex-start;'
        ),
        Div(id='test'),
        style=
        'display: flex; justify-content: left; align-items: center; flex-wrap: wrap; margin-top: 35px; padding: 10px 0;'  # Removed horizontal padding
    )


# def show_plots(session_id):
#     plot_conf = queryDB(session_id)
#     all_plots = Div(
#         get_plot_header(plot_conf),
#         Div(Div(
#             plot_default_scatter(plot_conf),
#             id='chart',
#             style=
#             'display: flex; justify-content: center; align-items: center; flex-wrap: wrap; border-radius: 10px; background-color: white; padding: 10px; margin-top: 20px; margin-left: 20px;'
#         ),
#             Div(plot_config_scatter(plot_conf),
#                 id='chart_config',
#                 style='width: 50%'),
#             style=
#             'display: flex; flex-wrap: wrap; flex-direction: row; justify-content: space-between; align-items: center; margin-top: 20px;',
#             id='plot_section'),
#         get_plot_footer(session_id),
#         Div(id='code', style="margin: 15px; padding; 2px;"),
#         cls='background-color-pico-code',
#         style=grid_section)
#     return all_plots


def show_plots(session_id):
    plot_conf = queryDB(session_id)
    all_plots = Div(get_plot_header(plot_conf),
                    Div(Div(plot_default_scatter(plot_conf),
                            id='chart',
                            style=plot_chart_style),
                        Div(plot_config_scatter(plot_conf),
                            id='chart_config',
                            style=plot_config_style),
                        style=plot_section_container_style,
                        id='plot_section'),
                    get_plot_footer(session_id),
                    Div(id='code', style="margin: 15px; padding: 2px;"),
                    cls='background-color-pico-code',
                    style=grid_section)
    return all_plots


def create_slider_group(label,
                        slider_id,
                        slider_type,
                        min_value,
                        max_value,
                        value,
                        name,
                        hx_post=None,
                        hx_target=None,
                        step=1):
    return Group(
        P(label + " ", style="width: 50px; margin: 0px;"),
        Input(
            type=slider_type,
            min=min_value,
            max=max_value,
            step=step,
            value=value,
            name=name,
            hx_post=hx_post,
            hx_target=hx_target,
            style=slider_css,
        ),
        cls='group_slider',
        style=
        'display: flex; justify-content: center; align-items: center; padding: 0px; margin: 0px; border: none; border-color: transparent'
    )


def get_marker_selector(plot_conf):
    form_name = 'form_config_scatter' if plot_conf.plot_type == "scatter" else 'form_config_line'
    marker_options = ['None', 'o', 's', 'v', 'D', 'd', 'p', 'h', 'H']
    marker_labels = [
        'None', 'Circle', 'Square', 'Triangle Down', 'Diamond', 'Thin Diamond',
        'Pentagon', 'Hexagon', 'Rotated Hexagon'
    ]
    marker_options.reverse()
    marker_labels.reverse()

    option_list = [
        Option('Select Marker type',
               value='Select',
               name='marker',
               disabled=True,
               selected=False,
               style='background-color: #EEEEEE;',
               form=form_name),
    ]

    for label, value in zip(marker_labels, marker_options):
        option_list.append(
            Option(label,
                   value=value,
                   name='marker',
                   selected=(value == plot_conf.marker),
                   form=form_name))

    config = Select(*option_list,
                    cls='cst_button',
                    form=form_name,
                    name='marker',
                    style='margin: 0px;')

    return Div(P("Marker Type ", style="margin: 0; font-size: 80%"),
               config,
               style=("display: flex; "
                      "justify-content: space-between; "
                      "align-items: center; "
                      "margin-top: 15px; "
                      "margin-bottom: 15px; "
                      "height: 50px; "))


def plot_conf_plot(plot_conf):
    this_session = plot_conf.session_id
    config = Form(
        hx_target='#chart',
        hx_post='/get_plot',
        hx_trigger='change',  # Ensure that changes trigger updates
        id=
        'form_config_line',  # Ensure form ID is consistent with marker selector
        hx_vals={"session_id": this_session},
    )(
        Div(Div(P("Data Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Randomize Data",
                       hx_target="#chart",
                       get=randomize_seed,
                       hx_vals={"session_id": this_session},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        create_slider_group(name='nr_points',
                            label="Number of points",
                            slider_id='nr_of_points',
                            slider_type='range',
                            value=int(plot_conf.nr_points),
                            min_value=1,
                            max_value=200),
        create_slider_group(name='noise',
                            label="Noise",
                            slider_id='noise',
                            slider_type='range',
                            value=plot_conf.noise,
                            step=0.1,
                            min_value=0,
                            max_value=1),
        Div(Div(P("Plot Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Toggle Splines",
                       hx_target="#chart",
                       get=toggle_splines,
                       hx_vals={"session_id": this_session},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        create_slider_group(name="line_thickness",
                            label="Line Thickness",
                            slider_id="line_thickness",
                            slider_type="range",
                            value=int(plot_conf.line_thickness),
                            min_value=1,
                            max_value=10),
        create_slider_group(name='alpha',
                            label="Alpha",
                            slider_id='alpha',
                            slider_type='range',
                            value=float(plot_conf.alpha),
                            min_value=0,
                            max_value=1,
                            step=0.1),
        get_marker_selector(plot_conf),  # Marker selector updated here
        create_slider_group(name='markersize',
                            label="Marker Size",
                            slider_id='markersize',
                            slider_type='range',
                            value=int(plot_conf.markersize),
                            min_value=0,
                            max_value=20),
    )

    return config


def plot_config_scatter(plot_conf):
    print("Plot_conf: ", plot_conf)
    this_session = plot_conf.session_id
    config = Form(
        hx_target='#chart',
        hx_post='/get_plot',
        hx_trigger='change',  # Ensure that changes trigger updates
        id='form_config_scatter',
        hx_vals={"session_id": this_session},
    )(
        Div(Div(P("Data Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Randomize Data",
                       hx_target="#chart",
                       get=randomize_seed,
                       hx_vals={"session_id": plot_conf.session_id},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        create_slider_group(name='nr_points',
                            label="Number of points",
                            slider_id='nr_of_points',
                            slider_type='range',
                            value=int(plot_conf.nr_points),
                            min_value=1,
                            max_value=200),
        create_slider_group(name='noise',
                            label="Noise",
                            slider_id='noise',
                            slider_type='range',
                            value=float(plot_conf.noise),
                            step=0.1,
                            min_value=0,
                            max_value=1),
        Div(Div(P("Plot Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Toggle Splines",
                       hx_target="#chart",
                       get=toggle_splines,
                       hx_vals={"session_id": plot_conf.session_id},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        create_slider_group(name='alpha',
                            label="Alpha",
                            slider_id='alpha',
                            slider_type='range',
                            value=float(plot_conf.alpha),
                            min_value=0,
                            max_value=1,
                            step=0.1),
        get_marker_selector(plot_conf),  # Marker selector updated here
        create_slider_group(name='size_scatter',
                            label="Scatter Size",
                            slider_id='size_scatter',
                            slider_type='range',
                            value=int(plot_conf.size_scatter),
                            min_value=0,
                            max_value=50),
    )

    return config


def plot_config_hist(plot_conf):
    print("Plot_conf: ", plot_conf)
    this_session = plot_conf.session_id
    config = Form(
        hx_target='#chart',
        hx_post='/get_plot',
        hx_trigger='change',  # Ensure that changes trigger updates
        id='form_config_hist',
        hx_vals={"session_id": this_session},
    )(
        Div(Div(P("Data Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Randomize Data",
                       hx_target="#chart",
                       get=randomize_seed,
                       hx_vals={"session_id": plot_conf.session_id},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        create_slider_group(name='nr_bins',
                            label="Number of bins",
                            slider_id='nr_of_bins',
                            slider_type='range',
                            value=int(plot_conf.nr_bins),
                            min_value=1,
                            max_value=50),
        create_slider_group(name='offset',
                            label="Offset",
                            slider_id='offset',
                            slider_type='range',
                            value=int(plot_conf.offset),
                            step=1,
                            min_value=0,
                            max_value=50),
        Div(Div(P("Plot Configurator",
                  cls='section_label',
                  style="margin: 0; align-self: center;"),
                style="flex: 1;"),
            Div(Button("Toggle Splines",
                       hx_target="#chart",
                       get=toggle_splines,
                       hx_vals={"session_id": plot_conf.session_id},
                       hx_swap="innerHTML",
                       cls='cst_button',
                       style='margin: 0;'),
                style=plot_config_btn_div_style),
            style=plot_config_style),
        Div(Button("Toggle Outline",
                   hx_target="#chart",
                   get=toggle_outlines,
                   hx_vals={"session_id": plot_conf.session_id},
                   hx_swap="innerHTML",
                   cls='cst_button',
                   style='margin: 0;'),
            style=plot_config_btn_div_style),
        create_slider_group(name='alpha',
                            label="Alpha",
                            slider_id='alpha',
                            slider_type='range',
                            value=float(plot_conf.alpha),
                            min_value=0,
                            max_value=1,
                            step=0.1),
    )

    return config


@app.post("/get_plot")
def get_plot(d: dict, session_id: str):
    _ = conf.update(Conf(**d))
    plot_conf = queryDB(session_id)
    return Div(plot_data(plot_conf))


@app.get("/toggle_splines")
def toggle_splines(session_id: str):
    plot_conf = queryDB(session_id)
    plot_conf.show_splines = not plot_conf.show_splines
    asyncio.run(
        update_db({
            "session_id": session_id,
            "show_splines": plot_conf.show_splines
        }))

    return Div(plot_data(plot_conf))


@app.get("/toggle_outlines")
def toggle_outlines(session_id: str):
    plot_conf = queryDB(session_id)
    plot_conf.show_outlines = not plot_conf.show_outlines
    asyncio.run(
        update_db({
            "session_id": session_id,
            "show_outlines": plot_conf.show_outlines
        }))
    print("outline:", plot_conf.show_outlines)
    return Div(plot_data(plot_conf))


# TODO REFACTOR TO INCLUDE A SINGLE FORM AND ENDPOINT
@app.get("/randomize_seed")
def randomize_seed(session_id: str):
    plot_conf = queryDB(session_id)
    plot_conf.seed = np.random.randint(1000)

    return Div(plot_data(plot_conf))


# @app.post("/update_plot_type")
# def update_plot_type(session_id: str, plot_type: str):
#     global conf
#     plot_type = plot_type.lower()
#     _ = conf.update(Conf(session_id=session_id, plot_type=plot_type))

#     return Div(
#         Div(Div(plot_default_scatter(queryDB(session_id)) if plot_type
#                 == 'scatter' else plot_default_plot(queryDB(session_id)),
#                 id='chart',
#                 style=plot_chart_style),
#             Div(plot_config_scatter(queryDB(session_id)) if plot_type
#                 == 'scatter' else plot_conf_plot(queryDB(session_id)),
#                 id='chart_config',
#                 style=plot_config_style),
#             style=plot_section_container_style,
#             id='plot_section'))

# @app.post("/update_plot_type")
# def update_plot_type(session_id: str, plot_type: str):
#     global conf
#     plot_type = plot_type.lower()
#     _ = conf.update(Conf(session_id=session_id, plot_type=plot_type))
#     plot_conf = queryDB(session_id)

#     # Map plot types to their respective default and config functions
#     plot_components = {
#         'scatter': (plot_default_scatter, plot_config_scatter),
#         'plot': (plot_default_plot, plot_conf_plot),
#         'histogram': (plot_default_hist, plot_config_hist)
#     }

#     if plot_type not in plot_components:
#         return Div(f"Unknown plot type: {plot_type}")

#     default_plot, config_plot = plot_components[plot_type]

#     return Div(
#         Div(Div(default_plot(plot_conf), id='chart', style=plot_chart_style),
#             Div(config_plot(plot_conf),
#                 id='chart_config',
#                 style=plot_config_style),
#             style=plot_section_container_style,
#             id='plot_section'))


@app.post("/update_plot_type")
def update_plot_type(session_id: str, plot_type: str):
    global conf
    plot_type = plot_type.lower()
    _ = conf.update(Conf(session_id=session_id, plot_type=plot_type))

    # TODO Make plot_config consistent either session_id or plot_conf
    if plot_type == 'scatter':
        return Div(Div(plot_default_scatter(queryDB(session_id)),
                       id='chart',
                       style=(update_plot_type_default_style)),
                   Div(plot_config_scatter(queryDB(session_id)),
                       id='chart_config',
                       style='width: 50%; margin-left: 50px;'),
                   style=(update_plot_type_conf_style),
                   id='plot_section')
    elif plot_type == 'plot':
        return Div(Div(plot_default_plot(queryDB(session_id)),
                       id='chart',
                       style=(update_plot_type_default_style)),
                   Div(plot_conf_plot(queryDB(session_id)),
                       id='chart_config',
                       style='width: 50%; margin-left: 50px;'),
                   style=(update_plot_type_conf_style),
                   id='plot_section')

    elif plot_type == "histogram":
        return Div(Div(plot_default_hist(queryDB(session_id)),
                       id='chart',
                       style=(update_plot_type_default_style)),
                   Div(plot_config_hist(queryDB(session_id)),
                       id='chart_config',
                       style='width: 50%; margin-left: 50px;'),
                   style=(update_plot_type_conf_style),
                   id='plot_section')
    elif plot_type == 'density':
        return H1("Density")


def plot_options(dropdown_name, cases):
    return (Option(f'{dropdown_name}', disabled='True', selected='',
                   value=''), *map(lambda c: Option(c, selected=True), cases))


@app.get('/plot_names')
def get(plot_names: str):
    return Select(*plot_options("Select Plot Type", plot_names),
                  name='plot_type',
                  form='plot_config',
                  cls='cst_button')


@app.post("/update_plot_data_type")
def update_plot_data_type(session_id, plot_data_type: str):
    global discrete_plot_types, continous_plot_types
    if plot_data_type == 'discrete':
        #TODO Extend so that changing also automatically changes the plot type
        return Form(get(discrete_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#plot_section",
                    hx_swap="innerHTML",
                    hx_vals={"session_id": session_id})
    elif plot_data_type == 'continous':
        return Form(get(continous_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#plot_section",
                    hx_swap="innerHTML",
                    hx_vals={"session_id": session_id})


def get_plot_header(plot_conf):
    return Div(
        H3("Visualization", style=h2_style),
        Div(Form(
            id='plot_data_type_config',
            hx_trigger='input',
            hx_post="/update_plot_data_type",
            hx_target='#plot_selector',
            hx_swap='outerHTML',
        ),
            Div(update_plot_data_type(plot_conf.session_id, "discrete"),
                id="plot_selector"),
            cls='plot_configurator'),
    )


#TODO once again repeating code, can we unify?


def plot_default_plot(plot_conf):
    return plot_data(plot_conf)


def plot_default_scatter(plot_conf):
    return plot_data(plot_conf)


def plot_default_hist(plot_conf):
    return plot_data(plot_conf)


@app.get("/get_code")
def return_code(session_id: str):
    conf = queryDB(session_id)
    color_list = ast.literal_eval(conf.color_list)
    code_text = color_list
    md = Div(f"""
    {code_text}
    """, cls='marked')
    # return Div(md, cls='container')
    return Div(Pre(Code(code_text)))


@app.get("/change_color_data_type")
def change_color_data_type(session_id: str, d: dict):
    plot_conf = queryDB(session_id)

    return Div(plot_conf.color_data_type)


def color_container(id, value, session_id):
    buttonid_hx = f"#color_container_{id}"
    buttonid = f"color_container_{id}"

    return Div(
        Button(Img(src='icons/minus.svg', style='padding: 20%;'),
               type="button",
               cls='background-color-pico',
               id=f"removeColorBtn_{id}",
               hx_post="/delete_color",
               hx_target=f"#color-picker-form",
               hx_swap="innerHTML",
               hx_vals={"session_id": session_id},
               style=remove_button_style),
        Input(
            type='color',
            id=f'color_{id}',  # Changed to ensure ID starts with 'color_'
            name=f'color_{id}',  # Added name attribute
            value=value,
            hx_post='/change_colors',
            hx_target="#chart",
            hx_trigger='input',
            hx_vals={"session_id": session_id},
            style=color_style),
        style="position: relative; margin: 3px;",
        id=buttonid)


def save_colors(**kwargs):
    session_id = kwargs.pop('session_id')
    plot_conf = queryDB(session_id)

    # Extract color values, ignoring non-color entries
    color_list = [
        value for key, value in kwargs.items() if key.startswith('color_')
    ]

    asyncio.run(
        update_db({
            "session_id": session_id,
            "color_list": str(color_list)
        }))

    return Div(plot_data(plot_conf))


@app.post("/change_colors")
def get_colors(d: dict):
    return save_colors(**d)


@app.post("/add_new_color")
def update_number_of_colors(session_id: str):
    global conf
    plot_conf = queryDB(session_id)
    nr_colors = plot_conf.nr_colors + 1
    color_list = ast.literal_eval(plot_conf.color_list)
    color_list.append('#000')
    _ = conf.update(
        Conf(session_id=session_id,
             color_list=str(color_list),
             nr_colors=nr_colors))

    plot_config_scatter(queryDB(session_id))
    return color_selector(session_id)


@app.post("/delete_color")
def delete_color(d: dict):
    plot_conf = queryDB(d["session_id"])
    color_list = plot_conf.color_list
    color_list = ast.literal_eval(color_list)
    nr_colors = plot_conf.nr_colors

    btn_id = list(d.keys())[-2]
    id = btn_id.split("_")[-1]
    color_list.pop(int(id))

    nr_colors -= 1
    _ = conf.update(
        Conf(session_id=d["session_id"],
             color_list=str(color_list),
             nr_colors=nr_colors))
    return color_selector(d["session_id"])


def color_selector_raw(session_id: str):
    plot_conf = queryDB(session_id)
    heading = H3("Color Picker", style=h2_style)
    color_list = ast.literal_eval(plot_conf.color_list)
    add = Div(Button(Img(src='icons/plus.svg', style='padding: 20%'),
                     type="button",
                     hx_post="/add_new_color",
                     cls='background-color-pico',
                     hx_target='#color-picker-form',
                     hx_swap='innerHTML',
                     hx_vals={"session_id": session_id},
                     style=color_selector_raw_add_button_style),
              style=color_selector_raw_add_div_style)
    color_containers = [
        color_container(id, value, session_id)
        for id, value in enumerate(color_list)
    ]

    color_grid = Form(hx_post="/change_colors",
                      hx_target="#chart",
                      hx_trigger="input",
                      hx_vals={"session_id": session_id
                               })(Div(*color_containers,
                                      add,
                                      id="color-picker-grid",
                                      cls='section',
                                      style=color_selector_raw_grid_style),
                                  id="color-picker-form")

    return heading, color_grid, add


def color_selector(session_id: str):
    heading, color_grid, add = color_selector_raw(session_id)
    return color_grid


serve()
