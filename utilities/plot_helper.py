""" 
Plot Helper
***********

Helper functions that are common for both matplotlib and plotly.
These help to define what to plot, to organize the data and to 
align the text in the plot.
"""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from utilities.csv_reader import Column, import_collider_data

# Main Plot Configurations  ----------------------------------------------------

class PlotConfiguration(Protocol):
    xcolumn: str
    ycolumn: str
    textposition: str
    label: str
    logscale: str


class EnergyConfiguration:
    xcolumn = Column.START_YEAR
    ycolumn = Column.COM_ENERGY
    textposition = Column.TEXTPOSITION_COME
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


class LuminosityOverEnergyConfiguration:
    xcolumn = EnergyConfiguration.ycolumn
    ycolumn = LuminosityConfiguration.ycolumn
    textposition = Column.TEXTPOSITION_LVCOME
    xlabel = EnergyConfiguration.ylabel
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
OTHER_SYMBOL = "square"

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
        ParticleTypeMap("electron-proton", "e-p+", r"$e^-p$", OTHER_SYMBOL, "#DD34BE"),
        ParticleTypeMap("muon-antimuon", "mu+mu-", r"$\mu^+\mu^-$", LEPTON_SYMBOL, "#9467bd"),
]

def check_all_types_accounted_for(data: pd.DataFrame = None) -> None:
    """Helper function to check if all particle types in the list are accounted for and hence will be plotted.
    
    Args:
        data (pd.DataFrame): DataFrame containing the accelerator timeline data.
    """
    if data is None: 
        data = import_collider_data()

    particle_types = [ptype.shorthand for ptype in PARTICLE_TYPES]
    missing = [ptype for ptype in set(data[Column.TYPE]) if ptype not in particle_types]

    if missing:
        raise ValueError("The following particle-types are missing, "
                         "please add them to the PARTICLE_TYPES list in utilities.plot_helper: "
                         f"{missing}")


# Text Positions ---------------------------------------------------------------

DEFAULT_TEXT_POSITION = "middle right"

# manual text orientation for CoM-Energy plots
SPECIAL_ORIENTATION_ENERGY = {
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
    "FCC-hh": "top center",
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
    "FCC-hh": "top center",
    "EIC": "middle left",
}

# manual text orientation for Lumi vs Energy plots
SPECIAL_ORIENTATION_LUMI_ENERGY = {
    "FPP 27TeV": "bottom right",
    "PEP": "bottom right",
    "PETRA": "bottom right",
    "Muon v1": "top center",
    "ISR": "top center",
    "HF2012 Higgs": "middle left",
    "CLIC1500": "bottom right",
    "CLIC3000": "top center",
    "HL-LHC": "middle left",
    "ILC v1": "top left",
    "ILC v2": "top center",
    "ILC v3": "top center",
    "CLIC380": "bottom center",
    "FCC-hh": "top center",
    "EIC": "bottom center",
}


def assign_textposition(data: pd.DataFrame) -> pd.DataFrame:
    """Create two columns, which will tell the plot where the text should be placed.
    

    Args:
        data (pd.DataFrame): DataFrame containing a Name column. 

    Returns:
        pd.DataFrame: DataFrame with the new Columns. 
    """
    data[Column.TEXTPOSITION_COME] = data[Column.NAME].apply(
        lambda name: SPECIAL_ORIENTATION_ENERGY.get(name, DEFAULT_TEXT_POSITION)
    )

    data[Column.TEXTPOSITION_LUMI] = data[Column.NAME].apply(
        lambda name: SPECIAL_ORIENTATION_LUMI.get(name, DEFAULT_TEXT_POSITION)
    )

    data[Column.TEXTPOSITION_LVCOME] = data[Column.NAME].apply(
        lambda name: SPECIAL_ORIENTATION_LUMI_ENERGY.get(name, DEFAULT_TEXT_POSITION)
    )
    return data