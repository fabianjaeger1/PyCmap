import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import random

def get_random_discrete_colors(n_colors=3, exclude_lists=None):
    """
    Returns a list of hex colors randomly selected from matplotlib's qualitative colormaps.

    Parameters:
    -----------
    n_colors : int
        Number of colors needed (default: 3)
    exclude_lists : list, optional
        List of colormap names to exclude from selection

    Returns:
    --------
    colors : list
        List of hex color values
    name : str
        Name of the selected colormap
    """

    # List of qualitative colormaps suitable for discrete data
    qualitative_colormaps = [
        'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
        'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
    ]

    # Remove excluded colormaps if specified
    if exclude_lists:
        qualitative_colormaps = [cm for cm in qualitative_colormaps 
                               if cm not in exclude_lists]

    # Randomly select a colormap
    cmap_name = random.choice(qualitative_colormaps)
    base_cmap = plt.cm.get_cmap(cmap_name)

    # Get the number of colors in the original colormap
    if hasattr(base_cmap, 'N'):
        max_colors = base_cmap.N
    else:
        max_colors = 256

    # Ensure we don't request more colors than available
    if n_colors > max_colors:
        raise ValueError(f"Requested {n_colors} colors but {cmap_name} only has {max_colors} colors")

    # Get evenly spaced colors from the colormap
    rgba_colors = base_cmap(np.linspace(0, 1, n_colors))

    # Convert RGBA to hex
    hex_colors = []
    for color in rgba_colors:
        # Convert RGB values to integers (0-255)
        rgb = tuple(int(val * 255) for val in color[:3])
        # Convert to hex format
        hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        hex_colors.append(hex_color)

    return hex_colors, cmap_name


