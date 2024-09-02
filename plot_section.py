from data import *
from fasthtml.common import *
import numpy as np
import matplotlib.colors as mcolors






def convert_colors(list_colors: list):
                                                 rgb_colors = [
                                                     mcolors.hex2color(color)
                                                     for color in list_colors
                                                 ]
                                                 cmap = mcolors.LinearSegmentedColormap.from_list(
                                                     "my_cmap",
                                                     rgb_colors,
                                                     N=256)
                                                 return cmap
