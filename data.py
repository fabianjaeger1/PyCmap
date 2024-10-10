# histogram
import numpy as np
import matplotlib.pyplot as plt
from fasthtml.common import *
from fh_matplotlib import matplotlib2fasthtml

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


# TODO: make it a fixed length and keep static only when adding more points do those get randomized
def get_classes(n: int = 100, nr_classes: int = 10):
    return np.random.randint(0, nr_classes, n)


# def get_2d_data(n: int = 100, seed: int = 0):
#     np.random.seed(seed)
#     x = np.random.normal(size=n)
#     y = np.random.normal(size=n)
#     return x, y

# def get_2d_data(n: int = 100, seed: int = 0, noise: float = 1.0):
#     """
#     Generate 2D data points with adjustable noise level.

#     Parameters:
#     n (int): Number of data points to generate.
#     seed (int): Random seed for reproducibility.
#     noise (float): Level of noise, where 0 means no noise, 1 is default, and >1 increases noise.

#     Returns:
#     x, y (ndarray): Two arrays of shape (n,) with 2D coordinates.
#     """
#     np.random.seed(seed)

#     return x, y


def get_2d_data(n: int = 100,
                nr_clusters: int = 3,
                seed: int = 0,
                noise: float = 1.0):
    """
    Generate 2D data points clustered around specified centers with adjustable noise level.
    Parameters:
    n (int): Total number of data points to generate.
    n_clusters (int): Number of clusters to generate.
    seed (int): Random seed for reproducibility.
    noise (float): Level of noise, where 0 means no noise, 1 is default, and >1 increases noise.

    Returns:
    x, y (ndarray): Two arrays of shape (n,) with 2D coordinates.
    """

    # n_clusters =
    np.random.seed(seed)

    # Generate cluster centers
    cluster_centers = np.random.rand(nr_clusters,
                                     2) * 10  # Random centers in range [0, 10)

    # Generate data points around each cluster center
    points_per_cluster = n // nr_clusters
    x, y = [], []

    for center in cluster_centers:
        # Generate points around the cluster center with added noise
        x_cluster = center[0] + np.random.normal(0, noise, points_per_cluster)
        y_cluster = center[1] + np.random.normal(0, noise, points_per_cluster)

        x.extend(x_cluster)
        y.extend(y_cluster)

    # Convert to numpy arrays
    return np.array(x), np.array(y)


def setup_figure(figsize=(10, 6), show_splines: bool = False):
    fig, ax = plt.subplots(figsize=figsize)

    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')

    if not show_splines:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both',
                       left=False,
                       top=False,
                       right=False,
                       bottom=False,
                       labelleft=False,
                       labeltop=False,
                       labelright=False,
                       labelbottom=False)

    return fig, ax


# @matplotlib2fasthtml
@fh_svg
def plot_scatter(x,
                 y,
                 classes,
                 marker: str = 'o',
                 figsize=(5, 5),
                 size_scatter: int = 5,
                 alpha: float = 1,
                 cmap='viridis',
                 show_splines: bool = False,
                 **kwargs):
    fig, ax = setup_figure(figsize, show_splines)
    ax.scatter(x,
               y,
               c=classes,
               s=size_scatter,
               marker=marker,
               alpha=alpha,
               cmap=cmap,
               **kwargs)


'''
line_thickness
noise
markers/without marker
alpha
'''

# config_plot = {
#     "line thickness": {type: "range", min: 1, max: 10, value: 1}
# }

markers = ['o', 's', 'v', 'D', 'd', '>', 'x', 'X', 'p']

# def generate_line_data(n: int = 100, noise: float = 0.1):
#     """
#     Generates x and y data points for a line plot with optional Gaussian noise.

#     Parameters:
#     - n (int): Number of data points.
#     - seed (int): Random seed for reproducibility.
#     - noise (float): Standard deviation of the Gaussian noise.

#     Returns:
#     - Tuple of arrays (x, y): Generated data points with noise.
#     """
#     np.random.seed(np.random.randint(0, 100))
#     x = np.linspace(0, 1, n)
#     y = np.linspace(0, 1, n) + np.random.normal(0, noise, n)
#     return x, y


def generate_line_data(n: int = 100,
                       noise: float = 0.1,
                       offset_range: float = 1.0):
    """
    Generates x and y data points for a plot with optional Gaussian noise and random offset.

    Parameters:
    - n (int): Number of data points.
    - noise (float): Standard deviation of the Gaussian noise.
    - offset_range (float): Range for the random offset.

    Returns:
    - Tuple of arrays (x, y): Generated data points with noise and offset.
    """
    np.random.seed(np.random.randint(0, 100))
    x = np.linspace(0, 1, n)
    y = np.random.normal(0, noise, n) + np.random.uniform(
        -offset_range, offset_range)
    return x, y


@fh_svg
def plot_line(x,
              y,
              color_list,
              figsize=(5, 5),
              linewidth: int = 20,
              noise: float = 0,
              marker: str = 'None',
              markersize: int = 5,
              linestyle: str = 'solid',
              show_splines: bool = False,
              alpha: float = 1,
              nr_points: int = 100,
              **kwargs):
    fig, ax = setup_figure(figsize, show_splines)
    for i in color_list:
        x, y = generate_line_data(n=nr_points)
        # print(x, y)
        print(i)
        ax.plot(x,
                y,
                color=i,
                linewidth=linewidth,
                alpha=alpha,
                marker=marker,
                markersize=markersize,
                **kwargs)
    # ax.plot(x, y, c=classes, linewidth=line_thickness, alpha=alpha, **kwargs)


'''
alpha
bins

'''

histtypes = ['bar', 'barstacked', 'step', 'stepfilled']


@fh_svg
def plot_histogram(x,
                   classes,
                   histtype: str = "stepfilled",
                   bins: int = 10,
                   figsize=(5, 5),
                   alpha: float = 0.8):
    fig, ax = setup_figure(figsize)
    ax.hist(x, bins=bins, histtype=histtype, alpha=alpha, **kwargs)


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
