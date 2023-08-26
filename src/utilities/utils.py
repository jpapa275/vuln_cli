"""
    Utility functions
"""

import pathlib
from datetime import date, datetime, timedelta
from pathlib import Path
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import yaml
from requests.exceptions import HTTPError
from colorama import Fore, Style, init


def vali_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%b")
        return date_text
    except ValueError as exc:
        raise ValueError(
            f'Incorrect date format, should be MMM-YYYY similar to today: {date.today().strftime("%b-%Y")}'
        ) from exc


def is_dead_zone():
    def find_patch_tuesday(month=date.today().month, year=date.today().year):
        """We will use the 12th day of any month as our base date because it
        happens to always fall on the same week as the second tuesday
        regardless of the month/year. Thus to determine the date of the second tuesday of any
        month we will first check the day of the week that the second tuesday
        falls on for that given month/year. 
        Next we will find what date that the Sunday in that same week
        falls on, then we add 2 days to that date to give us the exact date of the second tueday.
        so if the 12th day of the month lands on a Sunday(6) and
        The datetime module starts the week on Mon (0) by default, we add 1 then we get 7 which would throw our script off.
        To offset this we will set any day of the week provided by the datetime module that is greater than 6 to 0 (or Sunday).                
        """

        base_date = datetime.strptime(f"{month} 12 {year}", "%m %d %Y")  # type: ignore
        day_of_week = base_date.date().weekday() + 1

        if day_of_week > 6:
            day_of_week = 0

        return base_date - timedelta(days=day_of_week) + timedelta(days=2)

    patch_tuesday = find_patch_tuesday()
    today = date.today()
    date_list = pd.date_range(
        start=date.today().replace(day=1), end=patch_tuesday.date() - timedelta(days=1)
    ).to_frame(name="date", index=False)
    date_list.date = date_list.date.apply(lambda x: x.date())
    date_list = date_list.date.to_list()
    if today in date_list:
        return True
    return False


def set_month(date_string):
    """Checks the logic to see if current date is in the deadzone,
        if the date_string is current YYYY-MM
        and if it is then the date is changed to the previous month.
        Otherwise it passes the value through
    Returns:
        str: date_string in YYYY-MM format
    """
    now = datetime.strftime(datetime.now(), "%Y-%b")
    if is_dead_zone() and date_string == now:
        return datetime.strftime(datetime.now() - relativedelta(months=1), "%Y-%b")
    return date_string


def is_data_frame(data_frame: pd.DataFrame) -> bool:
    if isinstance(data_frame, pd.DataFrame):
        return True
    else:
        raise TypeError(
            f"Input is not a valid Pandas DataFrame.\nType: {type(data_frame)}"
        )


def make_dataframe(data_frame_list: list) -> pd.DataFrame:
    if isinstance(data_frame_list, list):
        data_frame = pd.DataFrame(data_frame_list)
        return data_frame
    else:
        raise TypeError(f"Input is not a list.\nType: {type(data_frame_list)}")


def make_request(url: str, headers: dict):
    try:
        req = requests.get(url, headers=headers, timeout=10)
        req.raise_for_status()
        return req.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")


def output_csv(data_frame: pd.DataFrame):
    filepath = pathlib.Path(__file__).resolve().parent
    if filepath.exists() and is_data_frame(data_frame):
        data_frame.to_csv(filepath)


def get_config():
    file_path = Path(__file__).resolve().parents[2].joinpath("config.yml")
    return file_path


def import_config(config_file_path=get_config().as_posix()):
    with open(config_file_path, "r", encoding="UTF-8") as file:
        return yaml.safe_load(file)


def output_df(data_frame):
    """Outputs the DF with a rounded grid format using tabulate

    Args:
        data_frame (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    if is_data_frame(data_frame):
        return data_frame.to_markdown(tablefmt="rounded_grid", index=False)


def validate_cve(cve_id):
    url = import_config(get_config().as_posix()).get("settings").get("urls").get("nvd")
    url = f"{url}{cve_id.upper()}"
    # make the call to NVD
    response = requests.get(url=url, timeout=5)
    if response.status_code == 200:
        if response.json().get("resultsPerPage") == 1:
            return True
    return False


def banner():
    init(wrap=False)
    print(
        Fore.RED
        + r""" 
 ___      ___ ___  ___  ___       ________   ________  ___       ___     
|\  \    /  /|\  \|\  \|\  \     |\   ___  \|\   ____\|\  \     |\  \    
\ \  \  /  / | \  \\\  \ \  \    \ \  \\ \  \ \  \___|\ \  \    \ \  \   
 \ \  \/  / / \ \  \\\  \ \  \    \ \  \\ \  \ \  \    \ \  \    \ \  \  
  \ \    / /   \ \  \\\  \ \  \____\ \  \\ \  \ \  \____\ \  \____\ \  \ 
   \ \__/ /     \ \_______\ \_______\ \__\\ \__\ \_______\ \_______\ \__\
    \|__|/       \|_______|\|_______|\|__| \|__|\|_______|\|_______|\|__|                                                                           
    """
    )
    print(Style.RESET_ALL)


def print_color(statement):
    init(autoreset=True)
    print(Fore.YELLOW + statement)
