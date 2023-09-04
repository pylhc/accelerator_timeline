"""
Interactive Accelerator Timeline
********************************

This script allows you to interactively explore the accelerator data,
either by running the script and viewing the plots in a browser,
by running the script in interactive-mode e.g. in vscode 
or by checking the from this script generated gallery.

To run the script, make sure your environment has the requirements 
of `requirements_interactive_charts.txt` installed.
"""
#%%
# Preparations 
# ------------
# 
# Import modules and define plotting function.
# This code is omitted in the interactive gallery, so that you can immediately enjoy the interactive plots below.
# Check `interactive.py <https://github.com/pylhc/accelerator_timeline/blob/master/interactive_charts.py>`_ 
# for the full example code.
#

# No code to see here in the interactive gallery or the generated jupyter notebook.
# sphinx_gallery_start_ignore
from pathlib import Path
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from IPython.display import HTML, display

from utilities.csv_reader import Column, import_collider_data
from utilities.plot_helper import (PARTICLE_TYPES, EnergyConfiguration, LuminosityConfiguration,
                                   LuminosityOverEnergyConfiguration, PlotConfiguration,
                                   assign_textposition, check_all_types_accounted_for)
from utilities.sphinx_helper import get_gallery_dir, is_interactive, is_sphinx_build

# Hack for rendering LaTeX in VSCode 
# (see https://github.com/microsoft/vscode-jupyter/issues/8131#issuecomment-1589961116)
if not is_sphinx_build() and is_interactive():
    display(HTML(
        '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
    ))

# Import Data ---
data = import_collider_data()
data = assign_textposition(data)
check_all_types_accounted_for(data)

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
        particle_mask = data[Column.TYPE] == particle_type.shorthand
        for has_been_built in (True, False):
            if has_been_built:
                builtmask, marker_suffix, legend = data[Column.BUILT], "", "built"
            else:
                builtmask, marker_suffix, legend = ~data[Column.BUILT], "-open", "not built"
            
            mask = particle_mask & builtmask

            fig.add_trace(go.Scatter(
                x=data.loc[mask & builtmask, configuration.xcolumn], 
                y=data.loc[mask & builtmask, configuration.ycolumn],
                name=legend,
                legendgroup=particle_type.name,
                legendgrouptitle_text=particle_type.latex,
                text=data.loc[mask, Column.NAME],
                textposition=data.loc[mask, configuration.textposition],
                mode="markers+text", 
                marker={"symbol": f"{particle_type.symbol}{marker_suffix}", 
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

    logx, logy = "x" in configuration.logscale, "y" in configuration.logscale
    fig.update_xaxes(
        title=configuration.xlabel, 
        type="log" if logx else "linear",
        dtick=1 if logx else 10, 
        minor=dict(dtick="D1" if logx else 1, ticks="outside"),
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        title=configuration.ylabel, 
        type="log" if "y" in configuration.logscale else "linear",
        ticks='outside',
        dtick=1 if logy else 10, 
        minor=dict(dtick="D1" if logy else None, ticks="outside", showgrid=False),
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        # tickformat='e',
    )
    fig.update_layout(
        plot_bgcolor='white',
    )
    return fig

# sphinx_gallery_end_ignore

#%%
# Energy Timeline
# ---------------
# 

fig_com = plot(data, EnergyConfiguration)
# sphinx_gallery_start_ignore
if not is_sphinx_build() and not is_interactive():
    fig_com.show()
fig_com
# sphinx_gallery_end_ignore

#%%
# Luminosity timeline
# -------------------
#

fig_lumi = plot(data, LuminosityConfiguration)
# sphinx_gallery_start_ignore
if not is_sphinx_build() and not is_interactive():
    fig_lumi.show()
fig_lumi
# sphinx_gallery_end_ignore

#%%
# Luminosity vs. Energy 
# ---------------------
#

fig_lumi_energy = plot(data, LuminosityOverEnergyConfiguration)
# sphinx_gallery_start_ignore
if not is_sphinx_build() and not is_interactive():
    fig_lumi_energy.show()
fig_lumi_energy
# sphinx_gallery_end_ignore

#%% 
# Save plots
# ----------
# 
# Save the plots as PDF and PNG.

output_dir = Path("images")
# sphinx_gallery_start_ignore
if is_sphinx_build():
    output_dir = get_gallery_dir()
# sphinx_gallery_end_ignore

plotly.io.write_image(fig_com, output_dir / "energy-plotly.pdf", format="pdf")
plotly.io.write_image(fig_com, output_dir / "energy-plotly.png", format="png")
plotly.io.write_image(fig_lumi, output_dir / "luminosity-plotly.pdf", format="pdf")
plotly.io.write_image(fig_lumi, output_dir / "luminosity-plotly.png", format="png")
plotly.io.write_image(fig_lumi_energy, output_dir / "luminosity-vs-energy-plotly.pdf", format="pdf")
plotly.io.write_image(fig_lumi_energy, output_dir / "luminosity-vs-energy-plotly.png", format="png")


# sphinx_gallery_thumbnail_path = 'gallery/luminosity-vs-energy-plotly.png'
