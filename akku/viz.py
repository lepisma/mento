import calendar
from typing import List

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from akku.types import Entry


def calendar_plot(entries: List[Entry]):
    """
    Plot entries on an interactive calendar.
    """

    fig, ax = plt.subplots()
    ax.set_xlim((1, 8))
    ax.set_ylim((1, 8))

    cal = calendar.Calendar(firstweekday=6)

    padding = 0.1
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        ax.text(i + 1.5, 7 + 0.2, day, ha="center", color="#aaaaaa", fontfamily="Lora", fontstyle="italic", fontsize=16)

    row = 1
    for dt in cal.itermonthdates(2021, 1):
        if dt.month != 1:
            continue

        weekday = dt.isoweekday()
        x_grid = 1 + (weekday % 7)
        y_grid = 7 - row

        x = x_grid + padding
        y = y_grid + padding
        side = 1 - 2 * padding

        rect = patches.FancyBboxPatch((x, y), side, side, boxstyle="Round, pad=0, rounding_size=0.05", facecolor="red", edgecolor="#eeeeee")
        ax.add_patch(rect)

        rect = patches.FancyBboxPatch((x_grid + 1 - side / 2, y_grid), side / 2, side / 2, boxstyle="Round, pad=0, rounding_size=0.05", color="white")
        ax.add_patch(rect)

        ax.text(x_grid + 1 - side / 4, y_grid + side / 4, f"{dt.day}", ha="center", va="center", color="#999999", fontfamily="Lora", fontstyle="italic", fontsize=14)

        if weekday == 6:
            row += 1

    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()
