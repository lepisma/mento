"""
Akku

Usage:
  akku stats [--orgzly-file=<orgzly-file>] [--org-journal-dir=<org-journal-dir>]
    [--org-list-file=<org-list-file>] [--output-file=<output-file>]

Options:
  --orgzly-file=<orgzly-file>           Orgzly style log file.
  --org-journal-dir=<org-journal-dir>   Org journal directory.
  --org-list-file=<org-list-file>       File with list entry items.
  --output-file=<output-file>           Output file to put stats in [default: stats.csv].
"""

import getpass

from docopt import docopt

import akku.stats as stats
from akku import __version__
from akku.parser import parse_list_journal, parse_org_journal, parse_orgzly


def main():
    args = docopt(__doc__, version=__version__)

    if args["--orgzly-file"] or args["--org-journal-dir"] or args["--org-list-file"]:
        entries = []

        if args["--orgzly-file"]:
            entries.extend(parse_orgzly(args["--orgzly-file"]))

        if args["--org-journal-dir"]:
            passphrase = getpass.getpass("Passphrase for Org Journal: ")
            entries.extend(parse_org_journal(args["--org-journal-dir"], passphrase))

        if args["--org-list-file"]:
            entries.extend(parse_list_journal(args["--org-list-file"]))

        df = stats.summarize_discrete_moods(entries).merge(
            stats.summarize_number_of_entries(entries),
            how="outer",
            on="day",
            suffixes=["mood", "n"]
        )
        df.to_csv(args["--output-file"], index=None)
    else:
        raise RuntimeError("Need at least one source to work on")
