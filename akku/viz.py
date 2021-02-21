import calendar
import datetime
from typing import Dict, List

import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def plot_year(year: int, colors: Dict[datetime.date, str]):
    """
    Plot a complete year using given mapping of date to color.
    """

    fig, axs = plt.subplots(4, 3)

    date_patches = []
    for i in range(0, 12):
        month = i + 1
        date_patches.extend(plot_month(axs[i // 3, i % 3], year, month, colors))

    fig.suptitle(f"{year}", color="#999999", fontfamily="Lora", fontsize="xx-large", x=0.9, y=0.95, ha="right")
    plt.show()


def dark_foreground(c) -> bool:
    """
    Tell whether the given background color needs a dark foreground.
    """

    r, g, b, a = matplotlib.colors.to_rgba(c)
    brightness = r * 0.299 + g * 0.587 + b * 0.114 + (1 - a)

    return brightness > (186 / 255)


def plot_month(ax: Axes, year: int, month: int, colors: Dict[datetime.date, str]) -> List[plt.Artist]:
    """
    Plot a month using given color mapping and return a list of rectangular
    patches mapping to days.

    Each patch has an extra `_data` property which contains date value.
    """

    ax.set_xlim((1, 8))
    ax.set_ylim((1, 9))

    cal = calendar.Calendar(firstweekday=6)

    padding = 0.0
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        ax.text(i + 1.5, 7 + 0.3, day, ha="center", color="#aaaaaa", fontfamily="Lora", fontsize="smaller")

    ax.text(8 - padding, 9 - padding, calendar.month_name[month], ha="right", va="top", color="#777777", fontfamily="Lora", fontstyle="italic", fontsize="medium")

    date_patches = []

    row = 1
    for dt in cal.itermonthdates(year, month):
        if dt.month != month:
            continue

        weekday = dt.isoweekday()
        x_grid = 1 + (weekday % 7)
        y_grid = 7 - row

        x = x_grid + padding
        y = y_grid + padding
        side = 1 - 2 * padding

        color = colors.get(dt, "white")
        text_color = "#777777" if dark_foreground(color) else "white"

        rect = patches.FancyBboxPatch((x, y), side, side, boxstyle="Round, pad=0, rounding_size=0.0", facecolor=color, edgecolor="#eeeeee", picker=True)
        ax.add_patch(rect)

        rect._data = {"date": dt}
        date_patches.append(rect)
        ax.text(x + side / 2, y + side / 2, f"{dt.day}", ha="center", va="center", color=text_color, fontfamily="Lora", fontsize="x-small")

        if weekday == 6:
            row += 1

    ax.axis("off")
    return date_patches
