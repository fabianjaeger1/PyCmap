from fasthtml.common import *
from great_tables import GT, html
from great_tables.data import sza
import numpy as np

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml

from data import *

css = Style('''
    #myid {color: red; background-color: yellow; }
    .myclass { color: blue; background-color: green; margin: 10px; }
    .mycontainer { display: flex; justify-content: center; }
    .color_picker { width: 50px; height: 75px; }
    #color-picker { width: 30vw ; margin: 10px; border: 3px solid #1C6EA4; }
    #plots { width: 60vw ; margin: 10px; border: 3px solid #1C6EA4;}
    #grid { display: grid; grid-template-columns: repeat(20, 20px); grid-template-rows: repeat(20, 20px);gap: 1px; }
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
        Div(show_plots(), cls="mycontainer")
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


@app.get("/update_nr_classes")
def update_classes(slider: int):
    # global nr_classes, classes
    # nr_classes = slider
    # todo initialize with a default number
    x, y = get_2d_data(nr_points)
    classes = get_classes(nr_classes=slider,
                          n=nr_points)  # Random class for each point
    print(nr_classes)
    return Div(plot_scatter(x, y, nr_classes=classes, s=s))


# @app.get("/update_scatter_sizes")
# def update_scatter_size(slider: int):
#     global s
#     s = slider
#     print(s)
#     return Div(plot_scatter(x, y, nr_classes=nr_classes, s=slider))


def show_plots():
    all_plots = Div(Input(type='range',
                          min='1',
                          max='20',
                          value='2',
                          get=update_classes,
                          hx_target='#chart',
                          name='slider_classes'),
                    Input(type='range',
                          min='1',
                          max='20',
                          value='2',
                          get=update_scatter_size,
                          hx_target='#chart',
                          name='slider_scatter_size'),
                    Div(id='chart'),
                    id="plots")
    return all_plots


serve()
