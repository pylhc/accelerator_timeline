""" 
Plot Helper
-----------

Helper functions that are common for both matplotlib and plotly.
These help to define what to plot, to organize the data and to 
align the text in the plot.
"""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from utilities.csv_reader import Column

# Main Plot Configurations  ----------------------------------------------------

class PlotConfiguration(Protocol):
    xcolumn: str
    ycolumn: str
    textposition: str
    label: str
    logscale: str


class CenterOfMassConfiguration:
    xcolumn = Column.START_YEAR
    ycolumn = Column.COM_ENERGY
    textposition = Column.TEXTPOSITION_COM
    xlabel = "Year"
    ylabel = "Center-of-Mass Energy [GeV]"
    logscale = "y"


class LuminosityConfiguration:
    xcolumn = Column.START_YEAR
    ycolumn = Column.LUMINOSITY
    textposition = Column.TEXTPOSITION_LUMI
    xlabel = "Year"
    ylabel = r"$\mathrm{Peak\;Luminosity}\;\left[\mathrm{cm}^{-2}\mathrm{s}^{-1}\right]$"
    logscale = "y"


class LuminosityOverCoMConfiguration:
    xcolumn = CenterOfMassConfiguration.ycolumn
    ycolumn = LuminosityConfiguration.ycolumn
    textposition = Column.TEXTPOSITION_LUMI
    xlabel = CenterOfMassConfiguration.ylabel
    ylabel = LuminosityConfiguration.ylabel
    logscale = "xy"


# Plotting Symbols, Text and Colors --------------------------------------------

@dataclass
class ParticleTypeMap:
    name: str
    shorthand: str
    latex: str
    symbol: str
    color: str 

HADRON_SYMBOL = "diamond"
LEPTON_SYMBOL = "circle"

PLOTLY_MPL_SYMBOL_MAP = {
    "diamond": "d",
    "circle": "o",
    "cross": "x",
    "square": "s",
}


PARTICLE_TYPES = [
        ParticleTypeMap("proton-proton", "p+p+", r"$pp$", HADRON_SYMBOL, "#d62728"),
        ParticleTypeMap("proton-antiproton", "p+p-", r"$p\bar{p}$", HADRON_SYMBOL, "#2ca02c"),
        ParticleTypeMap("electron-electron", "e-e-", r"$e^-e^-$", LEPTON_SYMBOL, "#1f77b4"),
        ParticleTypeMap("electron-positron", "e+e-", r"$e^+e^-$", LEPTON_SYMBOL, "#ff7f0e"),
        ParticleTypeMap("muon-antimuon", "mu+mu-", r"$\mu^+\mu^-$", LEPTON_SYMBOL, "#9467bd"),
]


# Text Positions ---------------------------------------------------------------

DEFAULT_TEXT_POSITION = "middle right"

# manual text orientation for CoM plots
SPECIAL_ORIENTATION_CoM = {
    "FPP 24TeV": "bottom right",
    "FPP 27TeV": "top right",
    "KEK-B": "bottom center",
    "ILC v1": "middle left",
    "FCC-ee Z": "bottom right",
    "FCC-ee ZH": "middle left",
    "ADONE": "middle left",
    "CBX": "middle left",
    "VEPP-2": "top right",
    "VEPP-3": "bottom right",
    "VEPP-4M": "top right",
    "Muon v1": "bottom right",
}

# manual text orientation for LUMI plots
SPECIAL_ORIENTATION_LUMI = {
    "VEPP-2M": "middle left",
    "DORIS": "top right",
    "PETRA": "middle left",
    "Muon v3": "top center",
    "HE-LHC": "middle left",
    "ILC v1": "bottom center",
    "ILC v2": "top center",
    "HF2012 Higgs": "bottom center",
    "HF2012 Z": "top right",
    "FPP 27TeV": "bottom right",
    "FCC-ee ZH": "middle left",
}


def assign_textposition(data: pd.DataFrame) -> pd.DataFrame:
    """Create two columns, which will tell the plot where the text should be placed.
    

    Args:
        data (pd.DataFrame): DataFrame containing a Name column. 

    Returns:
        pd.DataFrame: DataFrame with the new Columns. 
    """
    data[Column.TEXTPOSITION_COM] = data[Column.NAME].apply(
        lambda name: SPECIAL_ORIENTATION_CoM.get(name, DEFAULT_TEXT_POSITION)
    )

    data[Column.TEXTPOSITION_LUMI] = data[Column.NAME].apply(
        lambda name: SPECIAL_ORIENTATION_LUMI.get(name, DEFAULT_TEXT_POSITION)
    )
    return data