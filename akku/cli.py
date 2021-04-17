"""
Akku

Usage:
  akku <database> [(--no-refresh|--force-refresh)]

Options:
  --no-refresh                          If set, don't refresh before loading entries.
  --force-refresh                       Force refresh all sources before loading entries.

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

    if args["--force-refresh"]:
        store.refresh(force=True)
    elif args["--no-refresh"]:
        pass
    else:
        store.refresh()

    app = QApplication([])
    entries = sorted(store.entries, key=entry_dt)

    window = ui.QWindow(entries)
    window.show()

    sys.exit(app.exec_())
