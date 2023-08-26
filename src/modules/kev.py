""" 
KEV Utilities
"""

import pandas as pd

from src.utilities.utils import import_config, is_data_frame, validate_cve, output_df

# import from config.yml
config = import_config().get("settings")
KEV_URL = config.get("urls").get("cisa_kev")
COLUMNS = config.get("kev_columns")


def get_cisa_kev() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.Dataframe: KEV DF sorted by date_added
    """
    data_frame = pd.read_csv(KEV_URL)
    if is_data_frame(data_frame):
        data_frame.columns = data_frame.columns.str.replace(
            r"([A-Z]\w+$)", r"_\1", regex=True
        )
        data_frame.columns = data_frame.columns.str.lower()
        return data_frame.sort_values(by="date_added", ascending=False)


def show_kev(data_frame=get_cisa_kev()):
    if is_data_frame(data_frame):
        data_frame = data_frame[COLUMNS]
        return output_df(data_frame)


def search_kev_cve(search: str, data_frame=get_cisa_kev(), out_df=False):
    """_summary_

    Args:
        search (str): CVE search term like CVE-2023-0000
        data_frame (pd.DataFrame, optional): _description_. Defaults to get_cisa_kev().

    Returns:
        pd.DataFrame: Output of the dataframe to the cli
    """
    if search is not None and not isinstance(search, bool):
        search = search.upper()
        if is_data_frame(data_frame) and validate_cve(search):
            search_result = data_frame.cve_id.str.contains(
                search, case=False, regex=False
            ).any()
            if search_result is not True:
                df = data_frame[data_frame.cve_id.values == search]
                if out_df:
                    return output_df(df[COLUMNS])
                return output_df(df[COLUMNS])
            else:
                return search_result
        return pd.DataFrame()
