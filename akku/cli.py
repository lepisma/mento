"""
Akku

Usage:
  akku parse [--orgzly-file=<orgzly-file>] [--org-journal-dir=<org-journal-dir>]
    [--org-list-file=<org-list-file>] [--output-file=<output-file>]
  akku plot <entries-file> [--year=<year>]

Options:
  --orgzly-file=<orgzly-file>           Orgzly style log file.
  --org-journal-dir=<org-journal-dir>   Org journal directory.
  --org-list-file=<org-list-file>       File with list entry items.
  --output-file=<output-file>           Output file to put parsed entries in [default: entries.pkl].
  --year=<year>                         Year to plot.
"""

import datetime
import getpass
import pickle
import sys

import matplotlib.pyplot as plt
from docopt import docopt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QWidget)

import akku.stats as stats
import akku.viz as viz
from akku import __version__
from akku.parser import parse_list_journal, parse_org_journal, parse_orgzly


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
        app = QApplication([])

        with open(args["--output-file"], "rb") as fp:
            entries = pickle.load(fp)

        cmap = plt.get_cmap("RdBu")

        colors = {}
        for dt, v in stats.aggregate_by_date(entries, stats.aggregate_mean_mood).items():
            if v is not None:
                colors[dt] = cmap((v + 2) / 4)

        if args["--year"]:
            year = int(args["--year"])
        else:
            year = datetime.datetime.now().year
        fig = viz.plot_year(year, colors)

        window = QWidget()
        window.setWindowTitle("akku")

        layout = QHBoxLayout()
        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

        window.setLayout(layout)
        window.show()

        sys.exit(app.exec_())
