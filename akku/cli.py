"""
Akku

Usage:
  akku parse [--orgzly-file=<orgzly-file>] [--org-journal-dir=<org-journal-dir>]
    [--org-list-file=<org-list-file>] [--output-file=<output-file>]
  akku plot <entries-file>

Options:
  --orgzly-file=<orgzly-file>           Orgzly style log file.
  --org-journal-dir=<org-journal-dir>   Org journal directory.
  --org-list-file=<org-list-file>       File with list entry items.
  --output-file=<output-file>           Output file to put parsed entries in [default: entries.pkl].
"""

import getpass
import pickle

import matplotlib.pyplot as plt
from docopt import docopt

import akku.stats as stats
from akku import __version__
from akku.parser import parse_list_journal, parse_org_journal, parse_orgzly
from akku.viz import plot_year


def main():
    args = docopt(__doc__, version=__version__)

    if args["parse"]:
        if args["--orgzly-file"] or args["--org-journal-dir"] or args["--org-list-file"]:
            entries = []

            if args["--orgzly-file"]:
                entries.extend(parse_orgzly(args["--orgzly-file"]))

            if args["--org-journal-dir"]:
                passphrase = getpass.getpass("Passphrase for Org Journal: ")
                entries.extend(parse_org_journal(args["--org-journal-dir"], passphrase))

            if args["--org-list-file"]:
                entries.extend(parse_list_journal(args["--org-list-file"]))

            with open(args["--output-file"], "wb") as fp:
                pickle.dump(entries, fp)
        else:
            raise RuntimeError("Need at least one source to work on")

    elif args["plot"]:
        with open(args["--output-file"], "rb") as fp:
            entries = pickle.load(fp)

        cmap = plt.get_cmap("RdBu")

        colors = {}
        for dt, v in stats.aggregate_mood(entries).items():
            colors[dt] = cmap((v + 2) / 4)

        plot_year(2021, colors)
