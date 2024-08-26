from fasthtml.common import *
from great_tables import GT, html
from great_tables.data import sza
from matplotlib.pyplot import style
import numpy as np

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml

from data import *


def cst_slider():
    return Input


#.colors {border: none; background-color: transparent; margin-left: 100px; padding: 0px;}
css = Style('''
    :root { width: 100%; height: 100%; margin: 20px;}
    .mycontainer { display: flex; justify-content: center; width: 100%; margin: 0px; padding: 0px; flex-wrap: wrap;}
    #color-picker-grid { width: 30vw ; margin: 10px; gap: 10px; }
    .colors { background-color: #FFF; border: none; margin: 20px;}
    #plots { width: 60vw ; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    #color_selector { width: 40vw ; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    #grid { display: grid; grid-template-columns: repeat(20, 20px); grid-template-rows: repeat(20,         20px);gap: 1px; }
    #section { background-color: blue }
    .cell { width: 20px; height: 20px; border: 1px solid black; }
    .alive { background-color: green; }
    .dead { background-color: white; }
    .group_slider {border-color: transparent}}
    #chart { border-radius: 20px; padding: 20px; }
    .cst_button { border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding: 12px; font-weight: medium; font-size: 14px; width: 200px;}
    .icon_button {  border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding-left: 0px; font-weight: medium; font-size: 14px; width: 200px; }
    .plot_selector { width: 200px; border: none; outline: none; font-size: 14px; font-weight: medium; background-color: #EEEEEE; margin: 15px; border}
    .plot_configurator {
    display: flex; flex-direction:: column; border: none; outline: none; font-size: 14px; font-weight: medium; align-items: center; justify-content: right;
    }
''')

app, rt = fast_app(
    pico=False,
    hdrs=(Link(
        rel='stylesheet',
        href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
        type='text/css'),
          Link(rel='stylesheet',
               href='https://unpkg.com/normalize.css',
               type='text/css'), css))


@app.get("/")
def home():
    html = [
        Titled("PyCmap"),
        Div(color_selector(), show_plots(), cls="mycontainer")
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
nr_colors = 2
test_color = '#FFF000'
color_list = ['#FFA500', '#FFA500']

nr_classes = 1
classes = np.random.randint(0, nr_colors, nr_points)
s = 1
seed = 100

x, y = get_2d_data(nr_points)

# @app.get("/update_plot")
# def update_plots(slider_classes: int, slider_scatter_size: int):
#     global nr_points
#     print(slider_classes, slider_scatter_size)
#     x, y = get_2d_data(nr_points)
#     classes = get_classes(nr_classes=slider_classes, n=nr_points)
#     return Div(plot_scatter(x, y, classes=classes, s=slider_scatter_size))


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
    return Div(plot_scatter(x, y, classes=classes, size_scatter=s))


@app.get("/update_nr_classes")
def update_classes(slider_nr_classes: int):
    global nr_classes, nr_points, classes, s, x, y
    nr_classes = slider_nr_classes
    classes = get_classes(nr_classes=slider_nr_classes,
                          n=nr_points)  # Random class for each point
    return Div(plot_scatter(x, y, classes=classes, size_scatter=s),
               # P(f"nr_classes: {slider_classes}")
               )


@app.get("/update_nr_points")
def update_nr_points(slider_nr_points: int):
    global nr_classes, nr_points, classes, s, x, y, seed
    nr_points = slider_nr_points
    x, y = get_2d_data(slider_nr_points, seed=seed)
    classes = get_classes(nr_classes=nr_classes,
                          n=nr_points)  # Random class for each point
    return Div(plot_scatter(x, y, classes=classes, size_scatter=s),
               # P(f"nr_classes: {slider_classes}")
               )


@app.get("/update_scatter_sizes")
def update_scatter_size(slider_scatter_size: int):
    global s, nr_classes, classes, nr_points, x, y
    s = slider_scatter_size
    return Div(
        plot_scatter(x, y, classes=classes, size_scatter=slider_scatter_size),
        # P(f"scatter_size: {slider_scatter_size}")
    )


def plot_config_plot():
    config = Div(H1("Plot"))
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
                    name='slider_nr_points'),
              cls='group_slider'),
        Group(P("# Classes"),
              Input(type='range',
                    min='1',
                    title="Number of classes",
                    max='20',
                    value='2',
                    get=update_classes,
                    hx_target='#chart',
                    name='slider_nr_classes'),
              cls='group_slider'),
        Group(P("Size Scatter"),
              Input(type='range',
                    min='1',
                    max='100',
                    value='50',
                    get=update_scatter_size,
                    hx_target='#chart',
                    name='slider_scatter_size'),
              cls='group_slider')),
    return config


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


discrete_plot_types = ['Scatter', 'Plot', 'Histogram']
continous_plot_types = ["Density", "Heatmap"] 


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
        Div(Form(Select(Option("Discrete", value='discrete'),
                         Option("Continous", value='continous'),
                         name='plot_data_type',
                         form='plot_data_type_config',
                         cls='cst_button'),
                  id='plot_data_type_config',
                  hx_trigger='input',
                  hx_post="/update_plot_data_type",
                  hx_target='#plot_selector',
                  hx_swap='innerHTML'),
             Div(update_plot_data_type("discrete"), id="plot_selector"),
        cls='plot_configurator'),
        style = "display: flex; justify-content: space-between; align-items: center;"
    )


def show_plots():
    all_plots = Div(
        get_plot_header(),
        Div(id='chart_config'),
        Div(id='chart'),
        Button(Img(
            src="icons/random.png",
            style=
            "width: 20px; height: 20px; margin-right: 5px; margin-left: 0px; padding-left: 0px;"
        ),
               "Randomize Data",
               hx_target="#chart",
               get=randomize_seed,
               hx_swap="innerHTML",
               cls='icon_button'),
        Button("Get Code", cls='cst_button'),
        id="plots")
    # all_plots = Div(Input(type='range',)
    return all_plots

def color_selector():
    section = Div(Grid(*update_number_of_colors(),
                       Button("x",
                              get=add_colors,
                              hx_target='#color-picker-grid',
                              hx_swap="innerHTML"),
                       id="color-picker-grid",
                       cls="mycontainer"),
                  id="color_selector")
    return section


@app.get('/add_colors')
def add_colors():
    global nr_colors
    global color_list
    nr_colors += 1
    color_list.append(f'#FFF')
    #button_js = """
    #var allcols = document.getElementsByClassName("colors");
    #var button = document.getElementById("add_clr_btn");
    #button.onclick = function() {
    #    for(var i = 0; i < allcols.length; i++) {
    #        allcols[i].style.backgroundColor = allcols[i].value;
    #}
    #"""
    return Grid(*update_number_of_colors(),
                Button("+",
                       get=add_colors,
                       hx_target='#color-picker-grid',
                       hx_swap="innerHTML",
                       id="add_clr_btn"),
                cls="mycontainer")


@app.get('/update_number_of_colors')
def update_number_of_colors():
    global nr_colors
    global color_list
    global test_color
    all_colors = []
    js = f"""
    var allcols = document.getElementsByClassName("colors");
    var color_list = {color_list};
    for(var i = 0; i < allcols.length; i++) {{
        allcols[i].value = color_list[i];
        allcols[i].style.backgroundColor = allcols[i].value;
        allcols[i].onchange = function() {{
            this.style.backgroundColor = this.value;
        }};
    }}
    """
    for i in range(nr_colors):
        id_name = "color" + str(i)
        current_color = color_list[i]
        print(test_color)
        this_color = Input(Script(js),
                           type="color",
                           id=id_name,
                           value=current_color,
                           hx_target = test_color,
                           cls='colors')
        all_colors.append(this_color)
    all_colors.append(Script(js))
    return all_colors


serve()
