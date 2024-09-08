from fasthtml.common import *
import numpy as np
import matplotlib.colors as mcolors

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml

from data import *
from plot_section import *
from color_section import *


def cst_slider():
    return Input


css = Style('''
    :root { width: 100%; height: 100%; margin: 0px; padding: 0px; data-theme: light;}
    .section_grid { display: flex; justify-content: center; width: 100%; margin: 20px; padding: 0px; flex-direction: row; flex-wrap: wrap; }
    .section { display: flex; justify-content: center; margin: 20px; padding: 0 }
    .color_section {display: flex; justify-content: flex-start; flex-direction: row; width: 40%; margin: 20px; padding: 0px; background-color: #F4F4F4; border-radius: 20px; }
    .plot_section { width: 50% ; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px; }
    #color-picker-grid { width: 30vw ; margin: 10px; gap: 10px; }
    .colors { background-color: #FFF; border: none; margin: 20px; border-radius: 15px;}
    #color_selector { width: 40vw ; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    .remove_color_btn {width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; font-size: 14px; margin: 0px; padding: 0px; border-radius: 50%;}
    .group_slider {border-color: transparent; display: flex; justify-content: center; align-items: center; margin: 10px; padding-left: 20px; border-radius: 20px;}}}
    #chart { border-radius: 20px; padding: 20px; }
    .cst_button { border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding: 12px; font-weight: medium; font-size: 14px; width: 200px; height: 45px; }
    .icon_button {  border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding-left: 0px; font-weight: medium; font-size: 14px; width: 200px; padding: 12px; height: 45px; }
    .plot_selector { width: 200px; border: none; outline: none; font-size: 14px; font-weight: medium; background-color: #EEEEEE; margin: 15px; border}
    .plot_configurator {
    display: flex; flex-direction:: column; border: none; outline: none; font-size: 14px; font-weight: medium; align-items: center; justify-content: right; flex-wrap: wrap;
    }
''')

slider_css = "width: 10px; background-color: #EEEEEE; margin: 15px; border-radius: 10px; border: none; outline: none;"

app, rt = fast_app(pico=True,
                   hdrs=(Link(rel='stylesheet',
                              href='css/pico.min.css',
                              type='text/css'),
                         Link(rel='stylesheet',
                              href='https://unpkg.com/normalize.css',
                              type='text/css'), picolink, MarkdownJS(),
                         HighlightJS(), css))

# app, rt = fast_app(hdrs = picolink, MarkdownJS(),
#                    HighlightJS())

# app = FastHTML(hdrs=(picolink, MarkdownJS(), HighlightJS()))


@app.get("/")
def home():
    html = [
        Titled("PyCmap"),
        Div(color_selector_init()(), show_plots(), cls="section_grid")
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

# GLOBAL VARIABLES
nr_points = 100
nr_colors = 3
test_color = '#FFF000'
color_list = ['#FFA500', '#FFC901', '#FFF000']
color_data_type = "rgb"

discrete_plot_types = ['Scatter', 'Plot', 'Histogram']
continous_plot_types = ["Density", "Heatmap"]

# nr_classes = 1
nr_classes = len(color_list)
classes = np.random.randint(0, nr_colors, nr_points)
s = 50
seed = 100
cmap = convert_colors(color_list)

x, y = get_2d_data(nr_points)

# @app.get("/update_plot")
# def update_plots(slider_classes: int, slider_scatter_size: int):
#     global nr_points
#     print(slider_classes, slider_scatter_size)
#     x, y = get_2d_data(nr_points)
#     classes = get_classes(nr_classes=slider_classes, n=nr_points)
#     return Div(plot_scatter(x, y, classes=classes, s=slider_scatter_size))


def create_slider_group(label,
                        slider_id,
                        slider_type,
                        min_value,
                        max_value,
                        value,
                        name,
                        hx_target=None,
                        get=None,
                        step=1):
    return Group(P(label + ": "),
                 Input(
                     type=slider_type,
                     min=min_value,
                     max=max_value,
                     value=value,
                     name=name,
                     get=get,
                     hx_target=hx_target,
                     style=slider_css,
                 ),
                 cls='group_slider')


def plot_config_plot():
    config = create_slider_group(name="line_thickness",
                                 label="Line Thickness",
                                 slider_id="line_thickness",
                                 slider_type="range",
                                 value=10,
                                 min_value=1,
                                 max_value=10)
    return config


def plot_config_hist():
    config = Div(H1("Histogram"))
    return config


def plot_config_scatter():
    config = Div(
        Group(P("# Points"),
              Input(type='range',
                    min='1',
                    title="Number of points",
                    max='200',
                    value='2',
                    get=update_nr_points,
                    hx_target='#chart',
                    name='slider_nr_points',
                    style=slider_css),
              cls='group_slider'),
        # Group(P("# Classes"),
        #       Input(type='range',
        #             min='1',
        #             title="Number of classes",
        #             max='20',
        #             value='2',
        #             get=update_classes,
        #             hx_target='#chart',
        #             name='slider_nr_classes',
        #             style=slider_css),
        #       cls='group_slider'),
        Group(P("Size Scatter"),
              Input(type='range',
                    min='1',
                    max='100',
                    value='50',
                    get=update_scatter_size,
                    hx_target='#chart',
                    name='slider_scatter_size',
                    style=slider_css),
              cls='group_slider'),
        style='background-color: #E8E8E8;'),
    return config


# REFACTOR TO INCLUDE A SINGLE FORM AND ENDPOINT
@app.get("/randomize_seed")
def randomize_seed():
    global nr_points
    global nr_colors
    global nr_classes
    global classes
    global s
    global seed
    # np.random.seed(np.random.randrange(1000))
    seed = np.random.randint(1000)
    x, y = get_2d_data(nr_points, seed=seed)
    classes = get_classes(nr_classes=nr_classes, n=nr_points)
    return Div(plot_scatter(x, y, classes=classes, size_scatter=s, cmap=cmap))


# @app.get("/update_nr_classes")
# def update_classes(slider_nr_classes: int):
#     global nr_classes, nr_points, classes, s, x, y, cmap
#     nr_classes = slider_nr_classes
#     classes = get_classes(nr_classes=slider_nr_classes,
#                           n=nr_points)  # Random class for each point
#     return Div(plot_scatter(x, y, classes=classes, size_scatter=s, cmap=cmap),
#                # P(f"nr_classes: {slider_classes}")
#                )


@app.get("/update_nr_points")
def update_nr_points(slider_nr_points: int):
    global nr_classes, nr_points, classes, s, x, y, seed, cmap
    nr_points = slider_nr_points
    x, y = get_2d_data(slider_nr_points, seed=seed)
    classes = get_classes(nr_classes=nr_classes,
                          n=nr_points)  # Random class for each point
    return Div(plot_scatter(x, y, classes=classes, size_scatter=s, cmap=cmap),
               # P(f"nr_classes: {slider_classes}")
               )


@app.get("/update_scatter_sizes")
def update_scatter_size(slider_scatter_size: int):
    global s, nr_classes, classes, nr_points, x, y, cmap
    s = slider_scatter_size
    return Div(
        plot_scatter(x,
                     y,
                     classes=classes,
                     size_scatter=slider_scatter_size,
                     cmap=cmap),
        # P(f"scatter_size: {slider_scatter_size}")
    )


@app.post("/update_plot_type")
def update_plot_type(plot_type: str):
    print(plot_type)
    if plot_type == 'Scatter':
        return plot_config_scatter()
    elif plot_type == 'Plot':
        return plot_config_plot()
    elif plot_type == "Histogram":
        return plot_config_hist()
    elif plot_type == 'Density':
        return H1("Density")


def plot_options(nm, cs):
    return (Option(f'{nm}', disabled='', selected='',
                   value=''), *map(Option, cs))


@app.get('/plot_names')
def get(plot_names: str):
    return Select(*plot_options('Select Plot Type', plot_names),
                  name='plot_type',
                  form='plot_config',
                  cls='cst_button')


@app.post("/update_plot_data_type")
def update_plot_data_type(plot_data_type: str):
    global discrete_plot_types, continous_plot_types
    print(plot_data_type)
    if plot_data_type == 'discrete':
        return Form(get(discrete_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#chart_config",
                    hx_swap="innerHTML")
        # return Form(Select(Option("Scatter", value='scatter'),
        #                 Option("Plot", value='plot'),
        #                 Option("Histogram", value='hist'),
        #                 name='plot_type',
        #                 form='plot_config',
        #                 cls='cst_button'),

    elif plot_data_type == 'continous':
        return Form(get(continous_plot_types),
                    id='plot_config',
                    hx_trigger='input',
                    hx_post="/update_plot_type",
                    hx_target="#chart_config",
                    hx_swap="innerHTML")


def get_plot_header():
    return Div(
        H2("Plot", style="margin: 10px; display: inline;"),
        Div(Form(
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
            Div(update_plot_data_type("discrete"), id="plot_selector"),
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


@app.get("/get_code")
def return_code():
    global color_list
    code_text = color_list
    md = Div(f"""
    {code_text}
    """, cls='marked')
    return Div(md, cls='container')


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
                   get=return_code),
            style=
            'display: flex; flex-direction: row; justify-content: right; align-items: center; flex-wrap: wrap;'
            ),
        Div(id='test'),
        style=
        'display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-top: 20px;'
    )


def show_plots():
    all_plots = Div(
        get_plot_header(),
        Div(plot_config_scatter(), id='chart_config'),
        Div(id='chart',
            style=
            'display: flex; justify-content: center; align-items: center; flex-wrap: wrap; border-radius: 10px; background-color: white; padding: 10px; margin-top: 20px;'
            ),
        get_plot_footer(),
        Div(id='code', style="margin: 15px; padding; 2px;"),
        cls="plot_section")
    # all_plots = Div(Input(type='range',)
    return all_plots


def color_container(id, value):
    buttonid_hx = f"#color_container_{id}"
    buttonid = f"color_container_{id}"
    return Div(Button(
        "-",
        type="button",
        cls="remove_color_btn",
        id=f"removeColorBtn_{id}",
        hx_post="/delete_color",
        hx_target=f"#{buttonid}",
        hx_swap="outerHTML",
        style=
        "position: absolute; top: 20px; left: 50px; z-index: 5; background-color: #8D8D8D; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); border-color: transparent"
    ),
               Input(
                   type='color',
                   id=id,
                   value=value,
                   cls='colors',
                   hx_post='/change_colors',
                   hx_trigger='input',
                   style=
                   "padding: 0px; border-radius: 15px; border-color: transparent;"
               ),
               style="position: relative;",
               id=buttonid)


def save_colors(**kwargs):
    global color_list, cmap, nr_classes, s, classes, nr_points, x, y
    # with open('colors.txt', 'w') as f:
    #     for key, value in kwargs.items():
    #         f.write(f'{key} = {value}\n')
    for key, value in kwargs.items():
        print(key)
        color_list[int(key)] = value
    cmap = convert_colors(color_list)
    print(color_list)
    nr_classes = len(color_list)
    print("nr of classes: {}".format(nr_classes))
    classes = get_classes(nr_classes=nr_classes, n=nr_points)
    return Div(plot_scatter(x, y, classes=classes, cmap=cmap, size_scatter=s))


@app.post("/change_colors")
def get_colors(d: dict):
    return save_colors(**d)


@app.post("/add_new_color")
def update_number_of_colors():
    global nr_colors
    nr_colors += 1
    color_list.append('#FFF')
    print(nr_colors)
    print('added color')
    plot_config_scatter()
    return color_selector()


@app.post("/delete_color")
def delete_color(d: dict):
    global nr_colors
    global color_list
    btn_id = list(d.keys())[-1]
    id = btn_id.split("_")[-1]
    #print(color_list)
    color_list.pop(int(id))
    #print(color_list)
    #print(id)
    #print('deleting color')
    nr_colors -= 1


def color_selector_raw():
    global color_list
    heading = Div(H3("Color Picker"))

    add = Button("+",
                 type="button",
                 hx_post="/add_new_color",
                 hx_target='#color-picker-form',
                 hx_swap='innerHTML',
                 style='margin: 20px;')

    color_containers = [
        color_container(id, value) for id, value in enumerate(color_list)
    ]

    color_grid = Form(
        hx_post="/change_colors", hx_target="#chart", hx_trigger="input"
    )(Div(
        *color_containers,
        add,
        id="color-picker-grid",
        cls='section',
        style=
        "margin: 20px; display: flex; flex-wrap: wrap; justify-content: flex-start;"
    ),
      id="color-picker-form")

    return heading, color_grid, add


def color_selector_init():
    heading, color_grid, add = color_selector_raw()
    return Div(color_grid, cls='color_section')


def color_selector():
    heading, color_grid, add = color_selector_raw()
    return color_grid


serve()
