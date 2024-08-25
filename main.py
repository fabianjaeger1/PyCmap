from fasthtml.common import *
from great_tables import GT, html
from great_tables.data import sza
import numpy as np

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml

from data import *


def cst_slider():
    return Input


css = Style('''
    #myid {color: red; background-color: yellow; }
    .myclass { color: blue; background-color: green; margin: 10px; }
    .mycontainer { display: flex; justify-content: center;}
    .color_picker { width: 50px; height: 75px; }
    #color-picker { width: 30vw ; margin: 10px; border: 3px solid #1C6EA4; }
    #plots { width: 60vw ; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    #grid { display: grid; grid-template-columns: repeat(20, 20px); grid-template-rows: repeat(20,         20px);gap: 1px; }
    #section { background-color: blue }
    .cell { width: 20px; height: 20px; border: 1px solid black; }
    .alive { background-color: green; }
    .dead { background-color: white; }
''')

app, rt = fast_app(
    pico=False,
    hdrs=(Link(rel='stylesheet',
               href='https://unpkg.com/normalize.css',
               type='text/css'),
          Link(rel='stylesheet',
               href='https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css',
               type='text/css'), css))


@app.get("/")
def home():
    html = [
        Titled("PyCmap"),
        P("wow such pretty colors!", id="myid"),
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


# @app.get("/update_nr_points")
# def update_nr_points(slider_nr_points: int):
#     global s, nr_classes, classes, nr_points
#     x, y = get_2d_data(nr_points)
#     classes = get_classes(nr_classes=slider_classes,
#                           n=nr_points)
#     return Div(
#         plot_scatter(x, y, classes=classes, size_scatter = s),
#         # P(f"scatter_size: {slider_scatter_size}")
#     )
'''
FOR MILA: https://docs.fastht.ml/api/pico.html
Take a look at this 
colors = [Input(type="color", value=o) for o in ('#e66465', '#53d2c5', '#f6b73c')]
show(Grid(*colors))
'''


def show_plots():
    all_plots = Div(Button("Randomize",
                           hx_target="#chart",
                           get=randomize_seed,
                           hx_swap="innerHTML"),
                    Group(
                        P("# Points"),
                        Input(type='range',
                              min='1',
                              title="Number of points",
                              max='200',
                              value='2',
                              get=update_nr_points,
                              hx_target='#chart',
                              name='slider_nr_points')),
                    Group(
                        P("# Classes"),
                        Input(type='range',
                              min='1',
                              title="Number of classes",
                              max='20',
                              value='2',
                              get=update_classes,
                              hx_target='#chart',
                              name='slider_nr_classes')),
                    Group(
                        P("Size Scatter"),
                        Input(type='range',
                              min='1',
                              max='100',
                              value='50',
                              get=update_scatter_size,
                              hx_target='#chart',
                              name='slider_scatter_size')),
                    Div(id='chart'),
                    id="plots"),
    # all_plots = Div(Input(type='range',)
    return all_plots


def color_selector():
    section = Div(*update_number_of_colors(plus=False),
                  Button("x",
                         onclick=update_number_of_colors(plus=True),
                         hx_target='#color-picker'),
                  id="color-picker")
    return section


def update_number_of_colors(plus=False):
    global nr_colors
    if plus:
        nr_colors = nr_colors + 1
    all_colors = []
    for i in range(nr_colors):
        id_name = "color" + str(i)
        all_colors.append(
            Input(type="color",
                  id=id_name,
                  value="#FFA500",
                  cls='color_picker'))
    return all_colors


serve()
