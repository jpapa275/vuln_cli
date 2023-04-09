from datetime import datetime

import requests
from requests.exceptions import HTTPError

from src.modules.kev import get_cisa_kev
from src.utilities.utils import (is_data_frame, make_dataframe, output_df,
                                 set_month, vali_date)


def get_msrc(date_string=datetime.strftime(datetime.now(), "%Y-%b")):
    kev_df = get_cisa_kev()
    now = datetime.strftime(datetime.now(), "%Y-%b")
    if date_string is None:
        date_string = now
        print(f"No date given, using today's date {date_string}.")

    date_string = set_month(date_string=date_string)
    # print(f"datestring: {date_string}")
    update = vali_date(date_string)
    # print(f"validated date string: {date_string}")
    headers = {"Accept": "application/json"}
    base_url = "https://api.msrc.microsoft.com/cvrf/v2.0/"
    url = f"{base_url}cvrf/{update}"
    # print(f"url: {url}")
    data_frame = make_dataframe(make_msrc_list(
        make_msrc_request(url, headers=headers)))
    data_frame['in_kev'] = data_frame['cve'].isin(kev_df['cve_id'])
    return data_frame


def match_product_tree(products, product_id):
    output = []
    for pid in product_id:
        for product in products:
            if product.get("ProductID") == pid:
                output.append(p.get("Value"))
    return output


def make_msrc_list(msrc_request):
    msrc_list = []
    date = msrc_request.get('DocumentTracking').get(
        'Identification').get('ID').get('Value')
    for msrc_req in msrc_request.get("Vulnerability"):
        if msrc_req.get("Title").get("Value") is not None:
            if len(msrc_req.get("CVSSScoreSets")) > 0:
                cvss_score = msrc_req.get("CVSSScoreSets")[0].get("BaseScore")
            else:
                cvss_score = 0
            # find exploitation bool
            exploitation = bool("Exploited:Yes" in msrc_req.get("Threats")[-1].get(
                "Description"
            ).get(
                "Value"
            ).split(";"))
            new_dict = {
                "date": date,
                "title": msrc_req.get("Title").get("Value", "No Title Provided"),
                "cve": msrc_req.get("CVE"),
                "cvss_v3": cvss_score,
                "vuln_type": msrc_req.get("Threats")[0].get("Description").get("Value", "Not Assigned Yet"),
                "exploited": exploitation,
            }
            msrc_list.append(new_dict)
    return msrc_list


# Summary. Group by vuln type and get a count
def vuln_type_summary(data_frame):
    if is_data_frame(data_frame) and data_frame.empty is not True:
        return output_df(
            data_frame.vuln_type.value_counts()
            .rename_axis("vuln_type")
            .reset_index(name="count")
        )
    else:
        print("No Vulnerablities Found!")


def parse_criticals(data_frame):
    if is_data_frame(data_frame):
        crits = data_frame.loc[(data_frame["cvss_v3"] >= 9)]
        if not crits.empty:
            return output_df(crits)
        else:
            print("No Critical Vulnerablities Found!")


def parse_zero_days(data_frame):
    if is_data_frame(data_frame):
        df = data_frame.loc[data_frame.exploited == True]
        if not df.empty:
            return output_df(df)
        else:
            print("No Zero Day Vulnerablities Found!")


def parse_browsers(data_frame):
    if is_data_frame(data_frame):
        df = data_frame.loc[data_frame.title.str.contains("Chromium")]
        if not df.empty:
            return output_df(df)
        else:
            print("No Browser Vulnerablities Found!")


def make_msrc_request(url, headers):
    try:
        req = requests.get(url, headers=headers, timeout=10)
        req.raise_for_status()
        return req.json()
    except HTTPError as http_err:
        raise http_err
