"""
Interactive Accelerator Timeline
================================

This script allows you to interactively explore the accelerator data.
To run the script, make sure your environment has the requirements 
of `requirements_interactive.txt` installed.
"""
#%%
# Preparations ---
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go

from utilities.csv_reader import Column, import_collider_data
from utilities.plot_helper import (PARTICLE_TYPES, CenterOfMassConfiguration,
                                   LuminosityConfiguration, PlotConfiguration, assign_textposition)

# plotly.offline.init_notebook_mode()
plotly.io.renderers.default = "notebook_connected"

# Hack for rendering LaTeX in VSCode (see https://github.com/microsoft/vscode-jupyter/issues/8131#issuecomment-1589961116)
from IPython.display import display, HTML
display(HTML(
    '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
))

# Import Data ---
data = import_collider_data()
data = assign_textposition(data)

# Plotting Function ---
# This is the definition of the actual plotting function, 
# which creates the interactive plotly plots

def plot(data: pd.DataFrame, configuration: PlotConfiguration) -> go.Figure:
    """Generate interactive plots with plotly, based on the given configuration, 
    which defines the columns to use and the text positions.

    Args:
        data (pd.DataFrame): DataFrame containing the (modified) accelerator timeline data
        configuration (PlotConfiguration): See :class:`utilities.plot_helper.PlotConfiguration`

    Returns:
        go.Figure: plotly figure 
    """
    fig = go.Figure()

    for particle_type in PARTICLE_TYPES:
        mask = data[Column.TYPE] == particle_type.shorthand
        fig.add_trace(go.Scatter(
            x=data.loc[mask, configuration.xcolumn], 
            y=data.loc[mask, configuration.ycolumn],
            name=particle_type.latex,
            text=data.loc[mask, Column.NAME],
            textposition=data.loc[mask, configuration.textposition],
            mode="markers+text", 
            marker={"symbol": particle_type.symbol, 
                    "color": particle_type.color}, 
            customdata=np.transpose([
                data.loc[mask, Column.NAME],
                [particle_type.name] * sum(mask),
                data.loc[mask, Column.COM_ENERGY],
                data.loc[mask, Column.LUMINOSITY],
                data.loc[mask, Column.LENGTH],
                data.loc[mask, Column.YEARS],
                data.loc[mask, Column.INSTITUTE],
                data.loc[mask, Column.COUNTRY],
            ])
        ))

    fig.update_traces(
        hovertemplate="<br>".join([
            "%{customdata[0]} (%{customdata[6]}, %{customdata[7]})",
            "Particles: %{customdata[1]}",
            "Center-of-Mass Energy [GeV]: %{customdata[2]}",
            "Luminosity [cm^-2s^-1]: %{customdata[3]}",  # sadly plotly does not support latex in hover
            "Length [m]: %{customdata[4]}",
            "Operation: %{customdata[5]}",
        ]) + "<extra></extra>"
    )
    fig.update_xaxes(
        title=configuration.xlabel, 
        dtick=10, 
        minor=dict(dtick=1, ticks="outside"),
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        title=configuration.ylabel, 
        type="log",
        ticks='outside',
        dtick=1,
        minor=dict(dtick="D1", ticks="outside", showgrid=False),
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        # tickformat='e',
    )
    fig.update_layout(
        plot_bgcolor='white',
    )
    return fig

#%%
# Plotting ---
# Here, the plotting is performed for Center-of-Mass and Luminosity timelines.

fig_com = plot(data, CenterOfMassConfiguration)
plotly.io.show(fig_com)

fig_lumi = plot(data, LuminosityConfiguration)
plotly.io.show(fig_lumi)

#%% 
# Save plots
# ----------
# 
# Optionally, save the plots as PDF.

# plotly.io.write_image(fig_com, "center-of-mass-energy.pdf", format="pdf")
# plotly.io.write_image(fig_lumi, "peak-luminosity.pdf", format="pdf")
