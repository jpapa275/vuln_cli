#! /usr/bin/env python
"""CLI with csv output capability as well as filters to quickly list out RCE, crits etc...
"""
from time import sleep

from src.modules.kev import search_kev_cve  # , show_kev
from src.modules.msrc_updates import (get_msrc, parse_browsers,
                                      parse_criticals, parse_zero_days,
                                      vuln_type_summary)
from src.utilities.utils import banner, print_color
from src.utilities.cli_options import cli_args


def cli(args=cli_args()):
    """Main CLI

    Args:
        args (_type_, optional): Argparse options. Defaults to cli_args().
    """
    secs = 0.5
    banner()
    sleep(secs)
    # print_color(f"[*] Collecting MSRC results from {args.date}\n")
    if args.summary:
        print_color(
            f"[*] Getting the summary of MS vulnerabilities for {args.date}\n")
        sleep(secs)
        print(vuln_type_summary(get_msrc(date_string=args.date)))
    if args.criticals:
        print_color(
            f"[*] Getting the critical MS vulnerabilities for {args.date}\n")
        sleep(secs)
        print(parse_criticals(get_msrc(date_string=args.date)))
    if args.zero_days:
        print_color(
            f"[*] Getting the zero day MS vulnerabilities for {args.date}\n")
        sleep(secs)
        print(parse_zero_days(get_msrc(date_string=args.date)))
    if args.browsers:
        print_color(
            f"[*] Getting the Edge browser vulnerabilities for {args.date}\n")
        sleep(secs)
        print(parse_browsers(get_msrc(date_string=args.date)))
    if args.search_kev:
        print_color(f"[*] Searching KEV for CVE id {args.search_kev}\n")
        sleep(secs)
        print(search_kev_cve(search=args.search_kev))
