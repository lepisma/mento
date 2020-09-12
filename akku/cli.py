"""
Akku

Usage:
  akku plot entries --orgzly-file=<orgzly-file>

Options:
  --orgzly-file=<orgzly-file>     Orgzly style log file.
"""

from docopt import docopt

import akku.viz as viz
from akku import __version__
from akku.parser import parse_orgzly


def main():
    args = docopt(__doc__, version=__version__)
    entries = parse_orgzly(args["--orgzly-file"])
    viz.plot_entries(entries)
