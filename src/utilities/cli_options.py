# Argparse and Click options
###
import argparse
import sys
from datetime import datetime
from src.utilities.utils import set_month


def cli_args():
    parser = argparse.ArgumentParser(
        prog="vuln_cli",
        description="CLI to get patch tuesday results from MSRC's Security Update Guide. Also includes a handy function to search CISA's KEV list.")

    parser.add_argument(
        "-d",
        "--date",
        help="Date string for the report query in format YYYY-mmm. Ex: 2023-FEB",
        default=set_month(date_string=datetime.strftime(
            datetime.now(), "%Y-%b")),
        action='store',
    )

    parser.add_argument(
        "-s",
        "--summary",
        help="Summary of Vuln Types with count of each",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "-c",
        "--criticals",
        help="Summary of Critical vulns as defined by cvss_v3 score >= 9",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "-z",
        "--zero-days",
        help="Summary of Zero Days with count of each",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "-b",
        "--browsers",
        help="Summary of Browser vulns with count of each",
        default=False,
        action='store_true'
    )
    parser.add_argument('--search-kev', help='Search KEV for a particular CVE',
                        default=False,
                        nargs='?',
                        metavar='CVE ID',
                        action='store')

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    # print(args)
    return args


# These are the click options but you'll have to tweak the cli function code to leverage it.
# def summary(date):
#     """Summary of Vuln Types with count of each"""
#     print(f"Collecting MSRC results from {date}")
#     print(vuln_type(data_frame))


# def criticals(date):
#     """Summary of Critical vulns as defined by cvss_v3 score >= 9 and vuln type is RCE"""
#     print(f"Collecting MSRC results from {date}")
#     df = parse_criticals(data_frame)
#     if df.empty:
#         print("No Criticals Found!")
#     else:
#         print(output_df(df))


# def zero_days(date):
#     """Summary of Zero Days with count of each"""
#     print(f"Collecting MSRC results from {date}")
#     df = parse_zero_days(data_frame)
#     if df.empty:
#         print("No Zero Days Found!")
#     else:
#         print(output_df(df))


# def browsers(date):
#     """Summary of Browser vulns with count of each"""
#     print(f"Collecting MSRC results from {date}")
#     brows_df = parse_browsers(data_frame)
#     if brows_df.empty:
#         print("No Browser Vulnerablities Found!")
#     else:
#         print(output_df(brows_df))


# def kev():
#     """Show CISA Known Exploited Vulnerabilities"""
#     print("Collecting KEV Results")
#     print(output_df(show_kev()))

# @cli.command()
# @click.argument('cve_id', nargs=1)
# def search_kev(cve_id):
#     """Show CISA Known Exploited Vulnerabilities"""
#     print(f"Searching KEV for {cve_id}")
#     results = search_kev_cve(search=cve_id, out_df=True)
#     if results.empty:
#         click.echo(
#             f"No results found in NVD or KEV for {cve_id}. Check that the cve_id spelling is valid")
#     else:
#         click.echo(output_df(results))


# @click.group()
# @click.pass_context
# @click.option(
#     "-d",
#     "--date",
#     help="Date string for the report query in format YYYY-mmm. Ex: 2023-FEB",
#     default=datetime.strftime(datetime.now(), "%Y-%b"),
# )


# def cli(ctx, date):
#     """Get's and outputs MSRC Updates"""
#     ctx.ensure_object(dict)
#     # IF the date given is in the dead zone when the current date is between the 1st and Patch Tuesday date
#     if is_dead_zone():
#         date = datetime.strftime(
#             datetime.now() - relativedelta(months=1), "%Y-%b")
#     ctx.obj['date'] = date
#     ctx.obj['df'] = get_msrc(date_string=ctx.obj['date'])
#
#
# @cli.command()
# @click.pass_obj
# def summary(ctx):
#     """Summary of Vuln Types with count of each"""
#     click.echo(f"Collecting MSRC results from {ctx['date']}")
#     print(output_df(vuln_type(ctx['df'])))


# @cli.command()
# @click.pass_obj
# def criticals(ctx):
#     """Summary of Critical vulns as defined by cvss_v3 score >= 9 and vuln type is RCE"""
#     click.echo(f"Collecting MSRC results from {ctx['date']}")
#     if ctx is not None:
#         print(output_df(parse_criticals(ctx['df'])))
#     else:
#         print("No Criticals Found!")


# @cli.command()
# @click.pass_obj
# def zero_days(ctx):
#     """Summary of Zero Days with count of each"""
#     click.echo(f"Collecting MSRC results from {ctx['date']}")
#     if ctx is not None:
#         print(output_df(parse_zero_days(ctx['df'])))
#     else:
#         print("No Zero Days Found!")


# @cli.command()
# @click.pass_obj
# def browsers(ctx):
#     """Summary of Browser vulns with count of each"""
#     click.echo(f"Collecting MSRC results from {ctx['date']}")
#     if ctx is not None:
#         print(output_df(parse_browsers(ctx['df'])))
#     else:
#         print("No Browser Vulnerablities Found!")


# @cli.command()
# @click.pass_obj
# def cisa_kev(ctx):
#     """Show CISA Known Exploited Vulnerabilities"""
#     click.echo("Collecting KEV Results")
#     if ctx is not None:
#         print(output_df(show_kev()))


# @cli.command()
# @click.argument('cve_id', nargs=1)
# def search_kev(cve_id):
#     """Show CISA Known Exploited Vulnerabilities"""
#     click.echo(f"Searching KEV for {cve_id}")
#     results = search_kev_cve(search=cve_id, out_df=True)
#     if results.empty:
#         click.echo(
#             f"No results found in NVD or KEV for {cve_id}. Check that the cve_id spelling is valid")
#     else:
#         click.echo(output_df(results))
