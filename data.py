# histogram
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fasthtml.common import *
from fh_matplotlib import matplotlib2fasthtml

# @rt("/")
# @app.get("/")
# def get():
#     return (
#         Socials(
#             title="Vercel + FastHTML",
#             site_name="Vercel",
#             description="A demo of Vercel and FastHTML integration",
#             image="https://vercel.fyi/fasthtml-og",
#             url="https://fasthtml-template.vercel.app",
#             twitter_site="@vercel",
#         ),
#         Container(
#             Card(
#                 Group(
#                     P(
#                         "FastHTML is a new next-generation web framework for fast, scalable web applications with minimal, compact code. It builds on top of popular foundations like ASGI and HTMX. You can now deploy FastHTML with Vercel CLI or by pushing new changes to your git repository.",
#                     ), ),
#                 header=(Titled("FastHTML + Vercel")),
#                 footer=(P(
#                     A(
#                         "Deploy your own",
#                         href=
#                         "https://vercel.com/templates/python/fasthtml-python-boilerplate",
#                     ),
#                     " or ",
#                     A("learn more", href="https://docs.fastht.ml/"),
#                     "about FastHTML.",
#                 )),
#             ), ),
#     )

# Discrete Data Distribution

# Plot


def fh_svg(func):
    "show svg in fasthtml decorator"

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)  # calls plotting function
        f = io.StringIO()  # create a buffer to store svg data
        plt.savefig(f, format='svg', bbox_inches='tight')
        f.seek(0)  # beginning of file
        svg_data = f.getvalue()
        plt.close()
        return NotStr(svg_data)

    return wrapper


'''
scatter plot variables
nr_points
nr_classes
randomize_points
alpha
s
color_map
'''


def get_classes(n: int = 100, nr_classes: int = 10):
    return np.random.randint(0, nr_classes, n)


def get_2d_data(n: int = 100, seed: int = 0):
    np.random.seed(seed)
    x = np.random.normal(size=n)
    y = np.random.normal(size=n)
    return x, y


# data = get_2d_data(n=100)


# @matplotlib2fasthtml
@fh_svg
def plot_scatter(x,
                 y,
                 classes,
                 figsize=(5, 5),
                 size_scatter: int = 5,
                 alpha: float = 1,
                 cmap='viridis',
                 **kwargs):
    plt.figure(figsize=figsize)
    plt.scatter(x,
                y,
                c=classes,
                s=size_scatter,
                alpha=alpha,
                cmap=cmap,
                **kwargs)
    plt.colorbar()
    # return scatter


# @fh_svg
# def plot_heatmap(matrix,figsize=(6,7),**kwargs):
#   plt.figure(figsize=figsize)
#   sns.heatmap(matrix, cmap='coolwarm', annot=False,**kwargs)


def generate_scatter_plot(nr_points=100,
                          nr_classes=5,
                          figsize=(10, 10),
                          **kwargs):
    """
    Generates a scatter plot with a specified number of points and classes.

    Parameters:
    - nr_points (int): The number of points to plot.
    - nr_classes (int): The number of classes (colors) to use.
    """
    x, y = get_2d_data(nr_points, seed=2)

    # Assign a class to each point
    classes = np.random.randint(0, nr_classes,
                                nr_points)  # Random class for each point

    # Create a colormap with the number of specified classes
    cmap = plt.cm.get_cmap('viridis', nr_classes)

    # Create scatter plot
    plt.figure(figsize=figsize)
    scatter = plt.scatter(x, y, c=classes, s=100, alpha=1, cmap=cmap, **kwargs)
    plt.colorbar(scatter,
                 ticks=range(nr_classes))  # Show color scale with class ticks
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Scatter Plot with {nr_points} Points and {nr_classes} Classes')
    plt.show()


# @fh_svg
# def generate_scatter_plot(nr_points=100, nr_classes=5):

#     def plot_heatmap(matrix, figsize=(6, 7), **kwargs):
#         plt.figure(figsize=figsize)
#         sns.heatmap(matrix, cmap='coolwarm', annot=False, **kwargs)

# Example usage
# generate_scatter_plot(nr_points=200, nr_classes=7)


def get_plot():
    return


# Scatter plot


def get_scatter():
    return


# Bar Chart


def get_bar():
    return


#def plot_
