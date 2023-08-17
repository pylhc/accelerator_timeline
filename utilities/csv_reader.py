""" 
CSV Reader
----------

Functionality to gather the data from the CSV file into an easy-to-use format:
A pandas DataFrame. In addition, some manipulation on the data is done, so 
that all the required data for plotting is present in the frame.

"""
from datetime import datetime
import pandas as pd
from pathlib import Path
import numpy as np


MAIN_DIR = Path(__file__).parent.parent
CSV_PATH = MAIN_DIR / "accelerator-parameters.csv"

class Column:
    # Columns of the CSV
    NAME = "Name"
    INSTITUTE = "Institute"
    COUNTRY = "Country"
    START_YEAR = "Start"
    TYPE = "Type"
    END_YEAR = "End"
    ENERGY = "Energy"
    ENERGY_B2 = "Energy B2"
    LUMINOSITY = "Luminosity max peak"
    LENGTH = "Length"
    REFERENCES = "References"
    # Columns used in Code
    COM_ENERGY = "CoMEnergy"
    BUILT = "Built"
    FUTURE = "Future"
    YEARS = "Years"
    TEXTPOSITION_COME = "TextPositionCoME"
    TEXTPOSITION_LUMI = "TextPositionLumi"
    TEXTPOSITION_LVCOME = "TextPositionLvCoME"


def import_collider_data() -> pd.DataFrame:
    """Load the data from the CSV file and perform some additional data-filtering
    and calculations.

    Returns:
        pd.DataFrame: The loaded data in form of a DataFrame. 
    """
    #%% Import Data
    data = pd.read_csv(CSV_PATH, skiprows=[1])
    data = data[~data[Column.LUMINOSITY].isna()]  # filter non-colliders

    # Calculate Center-of-Mass Energy
    identical_beam = data[Column.ENERGY_B2].isna()
    data.loc[identical_beam, Column.COM_ENERGY] = 2*data.loc[identical_beam, Column.ENERGY]
    data.loc[~identical_beam, Column.COM_ENERGY] = 2 * np.sqrt(data.loc[~identical_beam, Column.ENERGY]*data.loc[~identical_beam, Column.ENERGY_B2])

    # Check for future colliders and convert year to int
    def year_range(args):
        start, end, built, future = args
        if not built:
            return f"{start} (Estimated)"
        
        if not end or np.isnan(end):
            if future:
                return f"{int(start)} - Unkown"
            else:
                return f"{int(start)} - Present"

        return f"{int(start)} - {int(end)}"

    data[Column.BUILT] = ~data[Column.START_YEAR].astype(str).str.endswith("*")
    data[Column.START_YEAR] = data[Column.START_YEAR].astype(str).str.replace("*", "").astype(int)
    data[Column.FUTURE] = data[Column.START_YEAR] > datetime.now().year
    data[Column.YEARS] = data[[Column.START_YEAR, Column.END_YEAR, Column.BUILT, Column.FUTURE]].agg(year_range, axis=1)

    return data