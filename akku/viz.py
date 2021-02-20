import calendar
import datetime
from typing import Dict

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def plot_year(year: int, colors: Dict[datetime.date, str]):

    fig, axs = plt.subplots(4, 3)

    for i in range(0, 12):
        month = i + 1
        plot_month(axs[i // 3, i % 3], year, month, colors)

    fig.suptitle(f"{year}", color="#999999", fontfamily="Lora", fontstyle="italic", fontsize="x-large", x=0.9, y=0.95, ha="right")
    plt.show()


def plot_month(ax: Axes, year: int, month: int, colors: Dict[datetime.date, str]):
    """
    """

    ax.set_xlim((1, 8))
    ax.set_ylim((1, 9))

    cal = calendar.Calendar(firstweekday=6)

    padding = 0.1
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        ax.text(i + 1.5, 8 + 0.3, day, ha="center", color="#aaaaaa", fontfamily="Lora", fontstyle="italic", fontsize="smaller")

    ax.text(8 - padding, 1 + padding, calendar.month_name[month], ha="right", va="bottom", color="#999999", fontfamily="Lora", fontstyle="italic", fontsize="medium")

    row = 1
    for dt in cal.itermonthdates(year, month):
        if dt.month != month:
            continue

        weekday = dt.isoweekday()
        x_grid = 1 + (weekday % 7)
        y_grid = 8 - row

        x = x_grid + padding
        y = y_grid + padding
        side = 1 - 2 * padding

        color = colors.get(dt, "white")

        rect = patches.FancyBboxPatch((x, y), side, side, boxstyle="Round, pad=0, rounding_size=0.02", facecolor=color, edgecolor="#eeeeee")
        ax.add_patch(rect)

        rect = patches.FancyBboxPatch((x_grid + 1 - side / 2, y_grid), side / 2, side / 2, boxstyle="Round, pad=0, rounding_size=0.05", color="white")
        ax.add_patch(rect)

        ax.text(x_grid + 1 - side / 4, y_grid + side / 4, f"{dt.day}", ha="center", va="center", color="#999999", fontfamily="Lora", fontstyle="italic", fontsize="smaller")

        if weekday == 6:
            row += 1

    ax.axis("off")
