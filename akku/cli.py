"""
Akku

Usage:
  akku plot entries [--orgzly-file=<orgzly-file>] [--org-journal-dir=<org-journal-dir>]
    [--org-list-file=<org-list-file>]

Options:
  --orgzly-file=<orgzly-file>           Orgzly style log file.
  --org-journal-dir=<org-journal-dir>   Org journal directory.
  --org-list-file=<org-list-file>       File with list entry items.
"""

from docopt import docopt

from akku import __version__
from akku.parser import parse_list_journal, parse_org_journal, parse_orgzly


def main():
    args = docopt(__doc__, version=__version__)

    if args["--orgzly-file"] or args["--org-journal-dir"] or args["--org-list-file"]:
        entries = []

        if args["--orgzly-file"]:
            entries.extend(parse_orgzly(args["--orgzly-file"]))

        if args["--org-journal-dir"]:
            entries.extend(parse_org_journal(args["--org-journal-dir"]))

        if args["--org-list-file"]:
            entries.extend(parse_list_journal(args["--org-list-file"]))

        print(entries)
        print(len(entries))
    else:
        raise RuntimeError("Need at least one source to work on")
