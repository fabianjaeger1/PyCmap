# histogram
from matplotlib.lines import lineMarkers
import numpy as np
import matplotlib.pyplot as plt
from fasthtml.common import *
from fh_matplotlib import matplotlib2fasthtml
import ast
from plot_section import *

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


def get_2d_data(n: int = 100,
                nr_clusters: int = 3,
                seed: int = 0,
                noise: float = 0.1):
    """
    Generate 2D data points clustered around specified centers with adjustable spread.

    Parameters:
    n (int): Total number of data points to generate.
    nr_clusters (int): Number of clusters to generate.
    seed (int): Random seed for reproducibility.
    noise (float): Level of noise, determining the spread around cluster centroids.
                   Lower values result in tighter clusters, higher values in more spread.

    Returns:
    x, y (ndarray): Two arrays of shape (n,) with 2D coordinates.
    """

    np.random.seed(seed)

    # Generate cluster centers
    cluster_centers = np.random.rand(nr_clusters,
                                     2) * 10  # Random centers in range [0, 10)

    # Calculate points per cluster
    points_per_cluster = n // nr_clusters
    remainder = n % nr_clusters

    x = np.empty(n)
    y = np.empty(n)

    start = 0
    for i, center in enumerate(cluster_centers):
        # Determine number of points for this cluster
        cluster_size = points_per_cluster + (1 if i < remainder else 0)
        end = start + cluster_size

        # Generate points around the cluster center
        x[start:end] = center[0] + np.random.normal(0, noise, cluster_size)
        y[start:end] = center[1] + np.random.normal(0, noise, cluster_size)

        start = end

    return x, y


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


markers = ['o', 's', 'v', 'D', 'd', '>', 'x', 'X', 'p']


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
def plot_histogram(color_list,
                   offset: int = 1,
                   bins: int = 10,
                   figsize=(5, 5),
                   alpha: float = 0.8,
                   show_splines: bool = False,
                   show_outlines: bool = False,
                   seed: int = 1,
                   **kwargs):

    fig, ax = setup_figure(figsize, show_splines=show_splines)
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
    for i, color in enumerate(color_list):
        mean = i * offset
        x = get_hist_data(color_list, seed, i, mean)
        if show_outlines:
            edge_color = 'black'
            histtype = 'bar'
        else:
            edge_color = color
            histtype = 'stepfilled'
        ax.hist(x,
                bins=bins,
                histtype=histtype,
                edgecolor=edge_color,
                alpha=alpha,
                color=color,
                **kwargs)


def get_hist_data(color_list, seed, i, mean=0):
    n = len(color_list)
    np.random.seed(seed + i)
    print(seed)
    x = np.random.normal(mean, 10, 1000)
    return x


def get_plot():
    return


# Scatter plot


def get_scatter():
    return


# Bar Chart


def get_bar():
    return


def plot_data(plot_conf):
    if plot_conf.plot_type == "plot":
        x, y = generate_line_data(plot_conf.nr_points,
                                  noise=float(plot_conf.noise))
        return plot_line(x,
                         y,
                         nr_points=int(plot_conf.nr_points),
                         color_list=ast.literal_eval(plot_conf.color_list),
                         marker=plot_conf.marker,
                         linewidth=int(plot_conf.line_thickness),
                         markersize=int(plot_conf.markersize),
                         show_splines=plot_conf.show_splines,
                         alpha=float(plot_conf.alpha))
    elif plot_conf.plot_type == "scatter":
        color_list = ast.literal_eval(plot_conf.color_list)
        cmap = convert_colors(color_list)
        classes = get_classes(nr_classes=len(color_list),
                              n=plot_conf.nr_points)
        x, y = get_2d_data(int(plot_conf.nr_points),
                           nr_clusters=plot_conf.nr_colors,
                           seed=plot_conf.seed,
                           noise=float(plot_conf.noise))
        return plot_scatter(x,
                            y,
                            classes=classes,
                            marker=plot_conf.marker,
                            show_splines=plot_conf.show_splines,
                            size_scatter=int(plot_conf.size_scatter),
                            alpha=float(plot_conf.alpha),
                            cmap=cmap)
    elif plot_conf.plot_type == "histogram":
        color_list = ast.literal_eval(plot_conf.color_list)
        return plot_histogram(color_list=color_list,
                              bins=plot_conf.nr_bins,
                              offset=plot_conf.offset,
                              alpha=float(plot_conf.alpha),
                              show_splines=plot_conf.show_splines,
                              show_outlines=plot_conf.show_outlines,
                              seed=plot_conf.seed)

