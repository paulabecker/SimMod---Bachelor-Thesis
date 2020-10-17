"""Utilities"""
import os
from typing import Union, List
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Data utilities

def load_data(tag: str, outdir: str="../results"):
    """Loads the data of a run"""
    data_path = os.path.join(outdir, tag, "results.csv")
    data = data = pd.read_csv(data_path, sep=',')
    return data

def load_config(tag: str, outdir: str="../results"):
    """Loads the configuration (dict) of a run"""
    config_path = os.path.join(outdir, tag, "configuration.yml")
    with open(config_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def load_run(tag: str, outdir: str="../results"):
    """Loads a run"""
    data = load_data(tag, outdir)
    config = load_config(tag, outdir)
    return data, config

# -----------------------------------------------------------------------------
# Plot utilities

def lineplot(df, *,
             x_data: str,
             y_data: str,
             ax=None,
             save_figure: bool=False,
             plot_kwargs: dict=None,
             save_kwargs: dict=None):
    """Performs a simple lineplot from a dataframe.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame
        x_data (str): The x-data label
        y_data (str): The y-data label
        ax (None, optional): A matplotlib axis to add the plot to
        save_figure (bool, optional): Whether to save the figure
        plot_kwargs (dict, optional): Passed to plt.plot
        save_kwargs (dict, optional): Passed to plt.savefig
    
    Returns:
        Tuple: (fig, ax)
    """
    # Prepare the configuration dicts
    plot_kwargs = plot_kwargs if plot_kwargs else {}
    save_kwargs = save_kwargs if save_kwargs else {}

    # If no axis specified use the current axis
    ax = ax if ax else plt.gca()

    # Extract x-data and y-data from the dataframe and make a simple lineplot
    x = df[x_data]
    y = df[y_data]

    ax.plot(x, y, **plot_kwargs)

    # Set labels
    ax.set_xlabel(x_data.replace('_', ' '))
    ax.set_ylabel(y_data.replace('_', ' '))

    if save_figure:
        plt.savefig(**save_kwargs)

    return plt.gcf(), ax

def lineplots_on_grid(df,
                      x_data: Union[str, List[str]],
                      y_data: Union[str, List[str]],
                      nrows: int,
                      ncols: int,
                      save_figure: bool=False,
                      subplot_kwargs: dict=None,
                      plot_kwargs: dict=None,
                      save_kwargs: dict=None):
    """Performs simple lineplots for each (x_data, y_data) pair given and
    aranges them on a grid.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame
        x_data (Union[str, List[str]]): The x-data label or a list of labels.
            If single label is given, the same x-data is used for all entries
            in `y_data`.
        y_data (Union[str, List[str]]): The x-data label or a list of labels.
            If set to '_all', all columns in `df` are selected.
        nrows (int): The number of rows
        ncols (int): The number of columns
        save_figure (bool, optional): Whether to save the figure
        subplot_kwargs (dict, optional): Passed to plt.subplots
        plot_kwargs (dict, optional): Passed to plt.plot
        save_kwargs (dict, optional): Passed to plt.savefig
    
    Returns:
        Tuple: (fig, axes)
    """
    # Prepare the configuration dicts
    subplot_kwargs = subplot_kwargs if subplot_kwargs else {}
    plot_kwargs = plot_kwargs if plot_kwargs else {}
    save_kwargs = save_kwargs if save_kwargs else {}

    if isinstance(x_data, str) and y_data=='_all':
        y_data = list(df.columns)

    # Prepare labels
    if isinstance(y_data, str):
        y_data = [y_data]
    if isinstance(x_data, str):
        x_data = [x_data] * len(y_data)
    elif len(x_data) != len(y_data):
        raise TypeError("'x_data' and 'y_data' must be of the same size. "
                        "Received: {} (x-data), {} (y-data)"
                        "".format(len(x_data), len(y_data)))

    fig, axes = plt.subplots(nrows, ncols, squeeze=False, **subplot_kwargs)
    axes = axes.ravel()

    # Plot each (x, y) pair in a new grid cell
    for i, (x, y) in enumerate(zip(x_data, y_data)):

        lineplot(df, x_data=x, y_data=y, ax=axes[i],
                 plot_kwargs=plot_kwargs)

        # Set labels
        axes[i].set_xlabel(x.replace('_', ' '))
        axes[i].set_ylabel(y.replace('_', ' '))

    if save_figure:
        fig.savefig(**save_kwargs)

    return fig, axes