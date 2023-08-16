""" 
Export Accelerator Timeline
---------------------------

"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from utilities.csv_reader import Column, import_collider_data
from utilities.plot_helper import (PARTICLE_TYPES, PLOTLY_MPL_SYMBOL_MAP, CenterOfMassConfiguration,
                                   LuminosityConfiguration, LuminosityOverCoMConfiguration,
                                   PlotConfiguration, assign_textposition)

MAIN_DIR = Path(__file__).parent

def plot(data: pd.DataFrame, configuration: PlotConfiguration) -> Figure:
    """Generate interactive plots with plotly, based on the given configuration, 
    which defines the columns to use and the text positions.

    Args:
        data (pd.DataFrame): DataFrame containing the (modified) accelerator timeline data
        configuration (PlotConfiguration): See :class:`utilities.plot_helper.PlotConfiguration`

    Returns:
        Figure: Matplotlib figure 
    """
    fig, ax = plt.subplots()
            
    pad = mpl.rcParams["lines.markersize"]/2
    vmap = {"top": pad, "middle": 0, "bottom": -pad}
    hmap = {"left": -pad, "center": 0, "right": pad}
    alignment_map = {"left": "right", "center": "center", "right": "left", "top": "bottom", "middle": "center", "bottom": "top"}

    for particle_type in PARTICLE_TYPES:
        mask = data[Column.TYPE] == particle_type.shorthand
        marker, fillstyle = PLOTLY_MPL_SYMBOL_MAP[particle_type.symbol]
        ax.plot(
            data.loc[mask, configuration.xcolumn], 
            data.loc[mask, configuration.ycolumn],
            linestyle="none",
            marker=marker, fillstyle=fillstyle,
            color=particle_type.color,
            label=particle_type.latex,
        )

        for x, y, text, textposition in zip(data.loc[mask, configuration.xcolumn], 
                                            data.loc[mask, configuration.ycolumn], 
                                            data.loc[mask, Column.NAME], 
                                            data.loc[mask, configuration.textposition]):
            v, h = textposition.split(" ")
            ax.annotate(text, xy=(x, y),  
                xytext=(hmap[h], vmap[v]), 
                textcoords="offset pixels", 
                ha=alignment_map[h], va=alignment_map[v]
            )

    ax.set_xlabel(configuration.xlabel)
    ax.set_ylabel(configuration.ylabel)
    for axis in ("x", "y"):
        if axis in configuration.logscale:
            getattr(ax, f"set_{axis}scale")("log")
            lim = getattr(ax, f"get_{axis}lim")()
            numticks = int(np.log10(lim[1]/lim[0])) + 1
            getattr(ax, f"{axis}axis").set_major_locator(plticker.LogLocator(base=10.0, numticks=numticks))
            getattr(ax, f"{axis}axis").set_minor_locator(plticker.LogLocator(base=10.0, subs=np.arange(2, 10)))
            getattr(ax, f"{axis}axis").set_minor_formatter(plticker.NullFormatter())
        else:
            getattr(ax, f"set_{axis}scale")("linear")
            getattr(ax, f"{axis}axis").set_major_locator(plticker.MultipleLocator(base=10.0))
            getattr(ax, f"{axis}axis").set_minor_locator(plticker.MultipleLocator(base=1.0))


    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0., title='Particles', ncol=1)
    return fig 


if __name__ == "__main__":
    plt.style.use(MAIN_DIR / "utilities" / "chart.mplstyle")
    output_dir = MAIN_DIR / "images"

    data = import_collider_data()
    data = assign_textposition(data)
    
    fig_com = plot(data, CenterOfMassConfiguration)
    fig_com.savefig(output_dir / "center-of-mass.pdf")
    fig_com.savefig(output_dir / "center-of-mass.png")

    fig_lumi = plot(data, LuminosityConfiguration)
    fig_lumi.savefig(output_dir / "luminosity.pdf")
    fig_lumi.savefig(output_dir / "luminosity.png")

    fig_lumi_vs_com = plot(data, LuminosityOverCoMConfiguration)
    fig_lumi_vs_com.savefig(output_dir / "luminosity-vs-CoM.pdf")
    fig_lumi_vs_com.savefig(output_dir / "luminosity-vs-CoM.png")

    # plt.show()