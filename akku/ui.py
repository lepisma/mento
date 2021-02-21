import datetime
from typing import List

import dominate.tags as T
import dominate.util
import orgpython
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QSplitter, QTextEdit, QWidget

from akku.types import Entry


class QJournal(QTextEdit):
    """
    Widget for displaying journal entries.
    """

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("QTextEdit { padding:10; border: none; }")
        self.font_family = "Lora"

    def format_entry_dt(self, entry: Entry) -> str:
        if entry.time:
            return datetime.datetime.combine(entry.date, entry.time).strftime("%b %d %Y %H:%M:%S")
        else:
            return entry.date.strftime("%b %d %Y")

    def format_entry(self, entry: Entry) -> str:
        div = T.div(style=f"font-family: {self.font_family}")

        div += T.div(self.format_entry_dt(entry), style="color: #999999; font-size: 13px;")
        div += T.br()

        body = dominate.util.raw(orgpython.to_html(entry.body.strip()))
        div += T.div(body, style="color: #555555; font-size: 13px;")

        div += T.br()
        div += T.br()
        div += T.br()

        return div.render()

    def render(self, entries: List[Entry]):
        for entry in entries:
            self.textCursor().insertHtml(self.format_entry(entry))


class QWindow(QWidget):
    """
    Main app window
    """

    def __init__(self, fig, entries):
        super().__init__()
        self.setWindowTitle("akku")
        self.setStyleSheet("background-color: white;")

        layout = QHBoxLayout()
        canvas = FigureCanvasQTAgg(fig)

        self.journal = QJournal()
        self.journal.render(entries)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(canvas)
        splitter.addWidget(self.journal)

        layout.addWidget(splitter)
        self.setLayout(layout)
