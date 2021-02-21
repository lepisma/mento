"""
Akku

Usage:
  akku parse [--orgzly-file=<orgzly-file>] [--org-journal-dir=<org-journal-dir>]
    [--org-list-file=<org-list-file>] [--output-file=<output-file>]
  akku <entries-file>

Options:
  --orgzly-file=<orgzly-file>           Orgzly style log file.
  --org-journal-dir=<org-journal-dir>   Org journal directory.
  --org-list-file=<org-list-file>       File with list entry items.
  --output-file=<output-file>           Output file to put parsed entries in [default: entries.pkl].
"""

import getpass
import pickle
import sys
from typing import List

from docopt import docopt
from PyQt5.QtWidgets import QApplication

import akku.ui as ui
from akku import __version__
from akku.parser import parse_list_journal, parse_org_journal, parse_orgzly
from akku.types import Entry
from akku.util import entry_dt


def parse_entries(orgzly_file=None, org_journal_dir=None, org_list_file=None) -> List[Entry]:
    if orgzly_file or org_journal_dir or org_list_file:
        entries = []

        if orgzly_file:
            entries.extend(parse_orgzly(orgzly_file))

        if org_journal_dir:
            passphrase = getpass.getpass("Passphrase for Org Journal: ")
            entries.extend(parse_org_journal(org_journal_dir, passphrase))

        if org_list_file:
            entries.extend(parse_list_journal(org_list_file))

        return entries
    else:
        raise RuntimeError("Need at least one source to work on")


def main():
    args = docopt(__doc__, version=__version__)

    if args["parse"]:
        entries = parse_entries(args["--orgzly-file"], args["--org-journal-dir"], args["--org-list-file"])
        with open(args["--output-file"], "wb") as fp:
            pickle.dump(entries, fp)

    else:
        app = QApplication([])

        with open(args["--output-file"], "rb") as fp:
            entries = sorted(pickle.load(fp), key=entry_dt)

        window = ui.QWindow(entries)
        window.show()

        sys.exit(app.exec_())
