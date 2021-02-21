import datetime
from typing import List

import dominate.tags as T
import dominate.util
import matplotlib.pyplot as plt
import numpy as np
import orgpython
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QSplitter, QTextEdit,
                             QToolButton, QVBoxLayout, QWidget)

import akku.stats as stats
import akku.viz as viz
from akku.types import Entry


class QJournal(QTextEdit):
    """
    Widget for displaying journal entries.
    """

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("QTextEdit { padding:10; border: none; background-color: transparent; }")
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


class QCalendar(FigureCanvasQTAgg):
    """
    Calendar plotted using matplotlib.
    """

    def __init__(self, entries):
        self.fig = plt.figure()
        super().__init__(self.fig)
        self.entries = entries

    def render(self, year: int, plot_type: str):
        self.fig.clear()

        colors = {}
        if plot_type == "polarity":
            ct = viz.color_transform((-1, 1))
            for dt, v in stats.aggregate_by_date(self.entries, stats.aggregate_mean_polarity).items():
                colors[dt] = ct(v)

        elif plot_type == "mood":
            ct = viz.color_transform((-2, 2))
            for dt, v in stats.aggregate_by_date(self.entries, stats.aggregate_mean_mood).items():
                if v is not None:
                    colors[dt] = ct(v)

        elif plot_type == "count":
            aggregated = stats.aggregate_by_date(self.entries, len)
            ct = viz.color_transform((0, max(aggregated.values())))
            for dt, v in aggregated.items():
                colors[dt] = ct(v)

        elif plot_type == "mentions":
            aggregated = stats.aggregate_by_date(self.entries, stats.aggregate_mentions)
            ct = viz.color_transform((0, max(aggregated.values())))
            for dt, v in aggregated.items():
                colors[dt] = ct(v)

        viz.plot_year(self.fig, year, colors)
        self.fig.canvas.draw_idle()


class QWindow(QWidget):
    """
    Main app window
    """

    def __init__(self, entries):
        super().__init__()
        self.setWindowTitle("akku")
        # self.setStyleSheet("background-color: white;")

        layout = QHBoxLayout()
        self.year = datetime.datetime.now().year
        self.plot_type = "mood"

        self.calendar = QCalendar(entries)
        self.refresh_calendar()

        self.journal = QJournal()
        self.journal.render(entries)

        side_pane = QWidget()
        side_pane_layout = QVBoxLayout()

        controls = QWidget()
        controls_layout = QHBoxLayout()

        left_button = QToolButton()
        left_button.setArrowType(Qt.LeftArrow)
        left_button.clicked.connect(self.left_click)

        right_button = QToolButton()
        right_button.setArrowType(Qt.RightArrow)
        right_button.clicked.connect(self.right_click)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["mood", "count", "polarity", "mentions"])
        self.combo_box.activated.connect(self.combo_click)

        controls_layout.addWidget(left_button)
        controls_layout.addWidget(right_button)
        controls_layout.addWidget(self.combo_box)
        controls.setLayout(controls_layout)

        side_pane_layout.addWidget(controls)
        side_pane_layout.addWidget(self.journal)
        side_pane.setLayout(side_pane_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.calendar)
        splitter.addWidget(side_pane)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def refresh_calendar(self):
        self.calendar.render(self.year, self.plot_type)

    def left_click(self):
        self.year -= 1
        self.refresh_calendar()

    def right_click(self):
        self.year += 1
        self.refresh_calendar()

    def combo_click(self):
        self.plot_type = self.combo_box.currentText()
        self.refresh_calendar()
