# Argparse and Click options
###
import argparse
import sys
from datetime import datetime

from src.utilities.utils import set_month


def cli_args():
    parser = argparse.ArgumentParser(
        prog="vuln_cli",
        description="CLI to get patch tuesday results from MSRC's Security Update Guide. Also includes a handy function to search CISA's KEV list.",
    )

    parser.add_argument(
        "-d",
        "--date",
        help="Date string for the report query in format YYYY-mmm. Ex: 2023-FEB",
        default=set_month(date_string=datetime.strftime(datetime.now(), "%Y-%b")),
        action="store",
    )

    parser.add_argument(
        "-s",
        "--summary",
        help="Summary of Vuln Types with count of each",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--criticals",
        help="Summary of Critical vulns as defined by cvss_v3 score >= 9",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "-z",
        "--zero-days",
        help="Summary of Zero Days with count of each",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "-b",
        "--browsers",
        help="Summary of Browser vulns with count of each",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--search-kev",
        help="Search KEV for a particular CVE",
        default=False,
        nargs="?",
        metavar="CVE ID",
        action="store",
    )

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    return args
