"""
Akku

Usage:
  akku <database>
  akku refresh <database>

Arguments:
  <database>                            Database keeping entries and source information.
"""

import sys

from docopt import docopt
from PyQt5.QtWidgets import QApplication

import akku.ui as ui
from akku import __version__
from akku.store import SQLiteStore
from akku.util import entry_dt


def main():
    args = docopt(__doc__, version=__version__)

    store = SQLiteStore(args["<database>"])

    if args["refresh"]:
        store.refresh()

    else:
        app = QApplication([])
        entries = sorted(store.entries, key=entry_dt)

        window = ui.QWindow(entries)
        window.show()

        sys.exit(app.exec_())
