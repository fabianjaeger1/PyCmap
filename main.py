from fasthtml.common import *
import numpy as np
import matplotlib.colors as mcolors
import uuid_utils as uuid

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml

from data import *
from plot_section import *
from color_section import *


session_conf = {}

# GLOBAL VARIABLES
conf_plot = {}
# plot_type: str = "scatter"

# BASE CONFIGURATION
conf_plot['plot_type'] = 'scatter'
conf_plot['nr_points'] = 100
conf_plot['alpha'] = 1
conf_plot['size_scatter'] = 5
conf_plot['marker'] = 'o'
conf_plot['line_thickness'] = 1
conf_plot['noise'] = 0
conf_plot['markersize'] = 4
conf_plot['nr_colors'] = 3
conf_plot['color_list'] = ['#FFA500', '#FFC901', '#FFF000']
conf_plot['color_data_type'] = "rgb"
conf_plot['test_color'] = '#FFF000'
conf_plot['cmap'] = convert_colors(conf_plot['color_list'])


def add_session(session_id):
    global session_conf, conf_plot
    session_conf[session_id] = conf_plot

def get_config(session_id):
    global session_conf
    return session_conf[session_id]

nr_colors = 3
test_color = '#FFF000'
color_list = ['#FFA500', '#FFC901', '#FFF000']
color_data_type = "rgb"
cmap = convert_colors(color_list)





def cst_slider():
    return Input


css = Style('''
    html {data-theme="light"}
    :root { width: 100%; height: 100%; margin: auto; margin-top: 5vh; padding: 0px; data-theme: light; max-width: 1500px;}
    .section_grid {display: grid; grid-template-columns:30% 70%; grid-gap: 0px;}
    .section { display: flex; justify-content: center; margin: 20px; padding: 0;}
    .color_section {display: flex; justify-content: flex-start; flex-direction: row; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px; }
    .plot_section { margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px; }
    #color-picker-grid { width: 30vw ; margin: 10px; gap: 10px; }
    .colors { background-color: #FFF; border: none; border-radius: 15px;}
    #color_selector { margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    .remove_color_btn {width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; font-size: 14px; margin: 0px; padding: 0px; border-radius: 50%;}
    .group_slider {border-color: transparent; display: flex; justify-content: center; align-items: center; margin: 10px; padding-left: 20px; border-radius: 20px; }}}
    #chart { border-radius: 20px; padding: 20px; }
    .cst_button { border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding: 12px; font-weight: medium; font-size: 14px; width: 200px; height: 45px; }
    .icon_button {  border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding-left: 0px; font-weight: medium; font-size: 14px; width: 200px; padding: 12px; height: 45px; }
    .plot_selector { width: 200px; border: none; outline: none; font-size: 14px; font-weight: medium; background-color: #EEEEEE; margin: 15px; border}
    .plot_configurator {
    display: flex; flex-direction:: column; border: none; outline: none; font-size: 14px; font-weight: medium; align-items: center; justify-content: right; flex-wrap: wrap;
    }
''')

slider_css = "width: 10px; margin: 15px; border-radius: 10px; border: none; outline: none;"

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='css/pico.min.css', type='text/css'),
        Link(rel='stylesheet',
             href='https://unpkg.com/normalize.css',
             type='text/css'),
        picolink,  ## uncomment to get dark mode
        MarkdownJS(),
        HighlightJS(),
        css))

# app, rt = fast_app(hdrs = picolink, MarkdownJS(),
#                    HighlightJS())

# app = FastHTML(hdrs=(picolink, MarkdownJS(), HighlightJS()))


# @app.get("/")
# def get(session):
#     if 'session_id' not in session: session['session_id'] = str(uuid.uuid4())
#     return H1(f"Session ID: {session['session_id']}")




@rt("/")
def home(session):
    if 'session_id' not in session: session['session_id'] = str(uuid.uuid4())
    print(session['session_id'])
    add_session(session['session_id'])
    # print(get_config(session['session_id']))
    conf_plot = get_config(session['session_id']) # pass this dictionary into the functions color_selector_init and show_plots
    # TODO Consider moving this into a database
    html = [
        Titled(f"PyCmap: {session['session_id']}"),
        Div((color_selector_init(conf_plot), show_plots(conf_plot)), cls="section_grid"),
        Footer(
            "Made with Love",
            style=
            'position: fixed; width: 100%; text-align: center; bottom: 0; left: 0; background-color: white; height:: 50px;'
        )
    ]
    return html

    # Div(Label(H3("Heatmap Columns"), _for='n_cols'),
    #    Input(type="range", min="1", max="10", value="1",
    #          get=update_heatmap, hx_target="#plot", id='n_cols'),
    #    Div(id="plot"))


# @app.get("/update_charts")
# def update_heatmap(n_cols:int):
#   svg_plot = plot_heatmap(data[:,:n_cols])
#   return svg_plot



# nr_points = 100


# discrete_plot_types = ['Scatter', 'Plot', 'Histogram']
discrete_plot_types = ['Histogram', 'Plot', 'Scatter']
continous_plot_types = ["Density", "Heatmap"]

# # nr_classes = 1
# nr_classes = len(color_list)
# classes = np.random.randint(0, nr_colors, nr_points)
# s = 50
# seed = 100

# x, y = get_2d_data(nr_points)

# @app.get("/update_plot")
# def update_plots(slider_classes: int, slider_scatter_size: int):
#     global nr_points
#     print(slider_classes, slider_scatter_size)
#     x, y = get_2d_data(nr_points)
#     classes = get_classes(nr_classes=slider_classes, n=nr_points)
#     return Div(plot_scatter(x, y, classes=classes, s=slider_scatter_size))

# def create_slider_group(label,
#                         slider_id,
#                         slider_type,
#                         min_value,
#                         max_value,
#                         value,
#                         name,
#                         hx_target=None,
#                         get=None,
#                         step=1):
#     return Group(P(label + ": "),
#                  Input(
#                      type=slider_type,
#                      min=min_value,
#                      max=max_value,
#                      value=value,
#                      name=name,
#                      get=get,
#                      hx_target=hx_target,
#                      style=slider_css,
#                  ),
#                  cls='group_slider')

# def custom_input(min_value, max_value, **kwargs):
#     return Div(
#         Input(type="range", min=min_value, max=max_value, **kwargs),
#         Div(P(min_value),
#             P(max_value),
#             style=
#             'display: flex; flex-direction: row; align-items: center; justify-content: space-between; margin: 0px; padding: 0px;'
#             ))


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
        P(label + " ", style="font-weight: bold; width: 50px; margin: 0px;"),
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
        # custom_input(min_value,
        #              max_value,
        #              value=value,
        #              name=name,
        #              step=step,
        #              hx_target=hx_target,
        #              hx_post=hx_post),
        cls='group_slider',
        style=
        'display: flex; justify-content: center; align-items: center; padding: 5px; margin: 5px;'
    )


def get_marker_selector():
    global conf_plot
    form_name = 'form_config_scatter'
    if conf_plot.get("plot_type") == "scatter":
        form_name = 'form_config_scatter'
    elif conf_plot.get("plot_type") == "plot":
        form_name = 'form_conf_plot'
    marker_options = ['None', 'o', 's', 'v', 'D', 'd', 'p', 'h', 'H']
    marker_labels = [
        'None', 'Circle', 'Square', 'Triangle', 'Diamond', 'Diamond',
        'Pentagon', 'Hexagon'
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
                   selected=True,
                   form=form_name), )
    config = Select(*option_list,
                    cls='cst_button',
                    form=form_name,
                    name='marker',
                    style='margin: 0px; backgroud-color: #EEEEEE;')
    # return config
    return Div(
        P("Marker Type ", style='font-weight: bold'),
        config,
        style=
        "display: flex; justify-content: space-between; align-items: center; padding: 5px; margin: 5px; height: 80px;"
    )


def plot_conf_plot(session_id: str):
    global conf_plot
    conf = conf_plot[session_id]
    config = Form(
        hx_target='#chart',
        hx_post='/get_lineplot',
        hx_trigger='change',
        id='form_config_line',
    )(
        create_slider_group(
            name="line_thickness",
            label="Line Thickness",
            slider_id="line_thickness",
            slider_type="range",
            value=int(conf['line_thickness']),
            min_value=1,
            # hx_post="/get_lineplot",
            # hx_target='#chart',
            max_value=10),
        create_slider_group(name='nr_points',
                            label="Number of points",
                            slider_id='nr_of_points',
                            slider_type='range',
                            value=int(conf['nr_points']),
                            min_value=1,
                            max_value=200),
        create_slider_group(name='alpha',
                            label="Alpha",
                            slider_id='alpha',
                            slider_type='range',
                            value=float(conf['alpha']),
                            min_value=0,
                            max_value=1,
                            step=0.1),
        create_slider_group(name='noise',
                            label="Noise",
                            slider_id='noise',
                            slider_type='range',
                            value=conf['noise'],
                            step=0.1,
                            min_value=0,
                            max_value=1),
        get_marker_selector(),
        create_slider_group(name='markersize',
                            label="Marker Size",
                            slider_id='markersize',
                            slider_type='range',
                            value=int(conf['markersize']),
                            min_value=0,
                            max_value=20),
    )

    return config


def plot_config_scatter(conf):
    print("Conf_scatter: {}".format(conf))
    config = Form(
        hx_target='#chart',
        hx_post='/get_scatterplot',
        hx_trigger='change',
        id='form_config_scatter',
    )(
        create_slider_group(name='nr_points',
                            label="Number of points",
                            slider_id='nr_of_points',
                            slider_type='range',
                            value=int(conf['nr_points']),
                            min_value=1,
                            max_value=200),
        create_slider_group(name='alpha',
                            label="Alpha",
                            slider_id='alpha',
                            slider_type='range',
                            value=float(conf['alpha']),
                            min_value=0,
                            max_value=1,
                            step=0.1),
        create_slider_group(name='noise',
                            label="Noise",
                            slider_id='noise',
                            slider_type='range',
                            value=float(conf['noise']),
                            step=0.1,
                            min_value=0,
                            max_value=1),
        get_marker_selector(),
        create_slider_group(name='scattersize',
                            label="Scatter Size",
                            slider_id='scattersize',
                            slider_type='range',
                            value=int(conf['size_scatter']),
                            min_value=0,
                            max_value=50),
    )

    return config


@app.post("/get_scatterplot")
def get_scatterplot(d: dict):
    global conf_plot
    conf_plot.update(d)
    global cmap, nr_points, color_list
    nr_points = int(d["nr_points"])
    #TODO: Add noise
    x, y = get_2d_data(nr_points)
    classes = get_classes(nr_classes=len(color_list), n=nr_points)
    print(classes)
    marker = d["marker"]
    print(marker)
    return Div(
        plot_scatter(x,
                     y,
                     classes=classes,
                     marker=marker,
                     size_scatter=int(d['scattersize']),
                     alpha=float(d['alpha']),
                     cmap=cmap))


@app.post("/get_lineplot")
def get_lineplot(d: dict):
    global conf_plot
    conf_plot.update(d)
    print(conf_plot)
    # global cmap, nr_points
    global cmap, nr_points
    nr_points = int(d["nr_points"])
    # print(line_thickness)
    # return Div("Hello")
    x, y = generate_line_data(nr_points, noise=float(d['noise']))
    return Div(
        plot_line(x,
                  y,
                  nr_points=nr_points,
                  color_list=color_list,
                  marker=conf_plot['marker'],
                  linewidth=d['line_thickness'],
                  markersize=d['markersize'],
                  alpha=float(d['alpha'])))
    # return Div(plot_line(x, y, s=10))


# def plot_conf_plot():
#     config = create_slider_group(name="line_thickness",
#                                  label="Line Thickness",
#                                  slider_id="line_thickness",
#                                  slider_type="range",
#                                  value=10,
#                                  min_value=1,
#                                  max_value=10)
#     return config


def plot_config_hist():
    config = Div(H1("Histogram"))
    return config


# def plot_config_scatter():
#     config = Div(
#         Group(P("# Points"),
#               Input(type='range',
#                     min='1',
#                     title="Number of points",
#                     max='200',
#                     value='2',
#                     get=update_nr_points,
#                     hx_target='#chart',
#                     name='slider_nr_points',
#                     style=slider_css),
#               cls='group_slider'),
#         # Group(P("# Classes"),
#         #       Input(type='range',
#         #             min='1',
#         #             title="Number of classes",
#         #             max='20',
#         #             value='2',
#         #             get=update_classes,
#         #             hx_target='#chart',
#         #             name='slider_nr_classes',
#         #             style=slider_css),
#         #       cls='group_slider'),
#         Group(P("Size Scatter"),
#               Input(type='range',
#                     min='1',
#                     max='100',
#                     value='50',
#                     get=update_scatter_size,
#                     hx_target='#chart',
#                     name='slider_scatter_size',
#                     style=slider_css),
#               cls='group_slider'),
#         style='background-color: #E8E8E8;'),
#     return config


# REFACTOR TO INCLUDE A SINGLE FORM AND ENDPOINT
@app.get("/randomize_seed")
def randomize_seed():
    global nr_colors
    global nr_classes
    global color_list
    global classes
    global seed
    global conf_plot

    nr_classes = len(color_list)

    if conf_plot['plot_type'] == "Plot":
        x, y = generate_line_data(int(conf_plot['nr_points']),
                                  noise=float(conf_plot['noise']))
        return Div(
            plot_line(x,
                      y,
                      nr_points=int(conf_plot['nr_points']),
                      color_list=color_list,
                      marker=conf_plot['marker'],
                      linewidth=int(conf_plot['line_thickness']),
                      markersize=int(conf_plot['markersize']),
                      alpha=float(conf_plot['alpha'])))
    elif conf_plot['plot_type'] == "Scatter":
        # np.random.seed(np.random.randrange(1000))
        seed = np.random.randint(1000)
        x, y = get_2d_data(int(conf_plot['nr_points']), seed=seed)
        classes = get_classes(nr_classes=nr_classes,
                              n=int(conf_plot['nr_points']))
        return Div(
            plot_scatter(x,
                         y,
                         classes=classes,
                         size_scatter=conf_plot['size_scatter'],
                         cmap=cmap))


# @app.get("/update_nr_classes")
# def update_classes(slider_nr_classes: int):
#     global nr_classes, nr_points, classes, s, x, y, cmap
#     nr_classes = slider_nr_classes
#     classes = get_classes(nr_classes=slider_nr_classes,
#                           n=nr_points)  # Random class for each point
#     return Div(plot_scatter(x, y, classes=classes, size_scatter=s, cmap=cmap),
#                # P(f"nr_classes: {slider_classes}")
#                )

# @app.get("/update_nr_points")
# def update_nr_points(slider_nr_points: int):
#     global nr_classes, nr_points, classes, s, x, y, seed, cmap
#     nr_points = slider_nr_points
#     x, y = get_2d_data(slider_nr_points, seed=seed)
#     classes = get_classes(nr_classes=nr_classes,
#                           n=nr_points)  # Random class for each point
#     return Div(plot_scatter(x, y, classes=classes, size_scatter=s, cmap=cmap),
#                # P(f"nr_classes: {slider_classes}")
#                )

# @app.get("/update_scatter_sizes")
# def update_scatter_size(slider_scatter_size: int):
#     global s, nr_classes, classes, nr_points, x, y, cmap
#     s = slider_scatter_size
#     return Div(
#         plot_scatter(x,
#                      y,
#                      classes=classes,
#                      size_scatter=slider_scatter_size,
#                      cmap=cmap),
#         # P(f"scatter_size: {slider_scatter_size}")
#     )


@app.post("/update_plot_type")
def update_plot_type(plot_type: str):
    global conf_plot
    conf_plot['plot_type'] = plot_type
    print(plot_type)
    if plot_type == 'Scatter':
        return plot_config_scatter()
    elif plot_type == 'Plot':
        return plot_conf_plot()
    elif plot_type == "Histogram":
        return plot_config_hist()
    elif plot_type == 'Density':
        return H1("Density")


def plot_options(dropdown_name, cases):
    return (Option(f'{dropdown_name}', disabled='', selected='',
                   value=''), *map(lambda c: Option(c, selected=True), cases))


@app.get('/plot_names')
def get(plot_names: str):
    return Select(*plot_options('Select Plot Type', plot_names),
                  name='plot_type',
                  form='plot_config',
                  cls='cst_button')


# @app.get('/plot_names')
# def get(plot_names: str):
#     return Select(*plot_options('Select Plot Type', plot_names),
#                   name='plot_type',
#                   form='plot_config',
#                   cls='cst_button')


@app.post("/update_plot_data_type")
def update_plot_data_type(conf, plot_data_type: str):
    print("Update_plot_data_type_conf: {}".format(conf))
    global discrete_plot_types, continous_plot_types
    print(plot_data_type)
    if plot_data_type == 'discrete':
        #TODO Extend so that changing also automatically changes the plot type
        return Form(get(discrete_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#chart_config",
                    hx_swap="innerHTML")
    elif plot_data_type == 'continous':
        return Form(get(continous_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#chart_config",
                    hx_swap="innerHTML")


def get_plot_header(conf):
    print(conf)
    return Div(
        H2("Plot", style="margin: 10px; display: inline;"),
        Div(Form(
            conf,
            Select(
                Option(
                    "Discrete",
                    value='discrete',
                ),
                Option("Continous", value='continous'),
                name='plot_data_type',
                form='plot_data_type_config',
                cls='cst_button',
            ),
            id='plot_data_type_config',
            hx_trigger='input',
            hx_post="/update_plot_data_type",
            hx_target='#plot_selector',
            hx_swap='innerHTML',
        ),
            Div(update_plot_data_type(conf, "discrete"), id="plot_selector"),
            cls='plot_configurator'),
        style=
        "display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap"
    )


# @app.route("/")
# def get():
#     title = 'Code Snippet Example'
#     code_text = open(__file__, 'r').read()
#     md = Div(f"""### Usage:
# ```python
# {code_text}
# ```""", cls='marked')
#     return Title(title), Main(H1(title), md, cls='container')

# @app.get("/get_code")
# def return_code():
#     code_text = "import matplotlib as plt"
#     md = Div(f"""### Usage:
#     ```python
#     {code_text}
#     ```""",
#              cls='marked')
#     return Main(md, cls='container')


def plot_default_scatter(conf):
    global conf_plot
    global cmap, color_list
    x, y = get_2d_data(n=int(conf_plot['nr_points']))
    nr_classes = len(color_list)
    nr_points = int(conf_plot['nr_points'])
    classes = get_classes(nr_classes=nr_classes, n=nr_points)
    return plot_scatter(x,
                        y,
                        classes=classes,
                        size_scatter=int(conf_plot['size_scatter']),
                        cmap=cmap)


@app.get("/get_code")
def return_code():
    global color_list
    code_text = color_list
    md = Div(f"""
    {code_text}
    """, cls='marked')
    # return Div(md, cls='container')
    return Div(Pre(Code(code_text)))


@app.get("/change_color_data_type")
def change_color_data_type():
    global color_data_type
    return Div(color_data_type)


def get_plot_footer():
    return Div(
        Div(Button(Img(
            src="icons/random.png",
            style=
            "width: 20px; height: 20px; margin-right: 5px; margin-left: 0px; padding-left: 0px;"
        ),
                   "Randomize Data",
                   hx_target="#chart",
                   get=randomize_seed,
                   hx_swap="innerHTML",
                   cls='icon_button'),
            style='disp'),
        Div(Form(Select(
            Option("Hex", value='hex'),
            Option("RGB", value='rgb', default=True),
            cls='cst_button',
        ),
                 hx_post="/change_color_data_type",
                 hx_target="#test"),
            Button("Get Code",
                   cls='cst_button',
                   hx_target="#code",
                   hx_swap='innerHTML',
                   get=return_code),
            style=
            'display: flex; flex-direction: row; justify-content: right; align-items: center; flex-wrap: wrap;'
            ),
        Div(id='test'),
        style=
        'display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-top: 20px;'
    )


def show_plots(conf):
    print(conf)
    all_plots = Div(
        get_plot_header(conf),
        Div(Div(
            plot_default_scatter(conf),
            id='chart',
            style=
            'display: flex; justify-content: center; align-items: center; flex-wrap: wrap; border-radius: 10px; background-color: white; padding: 10px; margin-top: 20px; margin-left: 20px;'
        ),
            Div(plot_config_scatter(conf), id='chart_config', style='width: 50%'),
            style=
            'display: flex; flex-wrap: wrap; flex-direction: row; justify-content: space-between; align-items: center; margin-top: 20px;'
            ),
        get_plot_footer(),
        Div(id='code', style="margin: 15px; padding; 2px;"),
        cls="plot_section")
    # all_plots = Div(Input(type='range',)
    return all_plots


def color_container(id, value):
    buttonid_hx = f"#color_container_{id}"
    buttonid = f"color_container_{id}"
    return Div(
        Button(
            "-",
            type="button",
            cls="remove_color_btn",
            id=f"removeColorBtn_{id}",
            hx_post="/delete_color",
            hx_target=f"#color-picker-form",
            hx_swap="innerHTML",
            style=
            "position: absolute; top: -3px; left: 60px; z-index: 5; background-color: #8D8D8D; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); border-color: transparent"
        ),
        Input(
            type='color',
            id=id,
            value=value,
            cls='colors',
            hx_post='/change_colors',
            hx_trigger='input',
            style=
            "padding: 0px; border-radius: 15px; border-color: transparent; height: 100px; width: 75px;"
        ),
        style="position: relative; margin: 3px;",
        id=buttonid)


def save_colors(**kwargs):
    # global color_list, cmap, nr_classes, s, classes, nr_points, x, y
    global color_list, cmap
    global conf_plot
    # with open('colors.txt', 'w') as f:
    #     for key, value in kwargs.items():
    #         f.write(f'{key} = {value}\n')
    # print(len(cmap))
    print(kwargs)
    print(len(color_list))
    for key, value in kwargs.items():
        color_list[int(key)] = value
    cmap = convert_colors(color_list)
    print(conf_plot['plot_type'])
    if conf_plot['plot_type'] == 'scatter':
        nr_classes = len(color_list)
        print("nr of classes: {}".format(nr_classes))
        x, y = get_2d_data(int(conf_plot['nr_points']))
        classes = get_classes(nr_classes=nr_classes, n=conf_plot['nr_points'])
        return Div(
            plot_scatter(x,
                         y,
                         classes=classes,
                         cmap=cmap,
                         size_scatter=conf_plot['size_scatter']))
    elif conf_plot['plot_type'] == 'plot':
        print("plot")
        nr_points = int(conf_plot["nr_points"])
        # print(line_thickness)
        # return Div("Hello")
        x, y = generate_line_data(nr_points, noise=float(conf_plot['noise']))
        return Div(
            plot_line(x,
                      y,
                      nr_points=nr_points,
                      color_list=color_list,
                      marker=conf_plot['marker'],
                      linewidth=conf_plot['line_thickness'],
                      markersize=conf_plot['markersize'],
                      alpha=float(conf_plot['alpha'])))


@app.post("/change_colors")
def get_colors(d: dict):
    return save_colors(**d)


@app.post("/add_new_color")
def update_number_of_colors(conf):
    global nr_colors
    nr_colors += 1
    color_list.append('#FFF')
    print(nr_colors)
    print('added color')
    plot_config_scatter()
    return color_selector()


@app.post("/delete_color")
def delete_color(d: dict):
    # global nr_colors
    # global color_list
    global conf
    btn_id = list(d.keys())[-1]
    id = btn_id.split("_")[-1]
    #print(color_list)
    color_list.pop(int(id))
    #print(color_list)
    #print(id)
    #print('deleting color')
    nr_colors -= 1
    return color_selector()


def color_selector_raw(conf):
    color_list= conf['color_list']
    heading = Div(H3("Color Picker"))

    add = Button(
        "+",
        type="button",
        hx_post="/add_new_color",
        hx_target='#color-picker-form',
        hx_swap='innerHTML',
        style=
        'height: 75px; width: 50px; margin-top: 12.5px;  margin-left: 12.5px; border-radius: 15px; background-color: #8D8D8D; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); border-color: transparent'
    )

    color_containers = [
        color_container(id, value) for id, value in enumerate(color_list)
    ]

    color_grid = Form(
        hx_post="/change_colors",
        hx_target="#chart",
        hx_trigger="input",
    )(Div(
        *color_containers,
        add,
        id="color-picker-grid",
        cls='section',
        style=
        "margin: 10px; display: flex; flex-wrap: wrap; justify-content: flex-start; width: 100%; padding-right: 5px; padding-left: 8px;"
    ),
      id="color-picker-form")

    return heading, color_grid, add


def color_selector_init(conf):
    print("Conf: {}".format(conf))
    heading, color_grid, add = color_selector_raw(conf)
    return Div(color_grid, cls='color_section')


def color_selector(conf):
    heading, color_grid, add = color_selector_raw(conf)
    return color_grid


serve()
