import calendar
import datetime
from typing import Any, Callable, Dict, List, Tuple

import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from pydash import py_

from akku.types import Entry


def color_transform(bounds: Tuple[Any, Any]) -> Callable[[Any], str]:
    """
    Make a transforming function that takes data from bounds to a color scale.
    """

    lb, ub = bounds

    if lb < 0:
        cmap = plt.get_cmap("RdBu")
    else:
        cmap = plt.get_cmap("Purples")

    return lambda v: cmap((v - lb) / (ub - lb))


def plot_year(fig: plt.Figure, year: int, colors: Dict[datetime.date, str]):
    """
    Plot a complete year using given mapping of date to color.
    """

    axs = [fig.add_subplot(4, 3, i) for i in range(1, 13)]

    date_patches = []
    for i in range(0, 12):
        month = i + 1
        date_patches.extend(plot_month(axs[i], year, month, colors))

    fig.suptitle(f"{year}", color="#999999", fontfamily="Lora", fontsize="xx-large", x=0.9, y=0.95, ha="right")


def plot_year_polar(fig: plt.Figure, year: int, entries: List[Entry]):
    axs = [fig.add_subplot(4, 3, i, projection="polar") for i in range(1, 13)]

    for i in range(0, 12):
        month = i + 1
        plot_month_polar(axs[i], year, month, entries, show_theta_labels=(month == 1))

    fig.suptitle(f"{year}", color="#999999", fontfamily="Lora", fontsize="xx-large", x=0.9, y=0.95, ha="right")


def plot_month_polar(ax: Axes, year: int, month: int, entries: List[Entry], show_theta_labels=True):
    items = []
    for e in entries:
        if not e.time:
            continue

        if e.date.month != month:
            continue

        if e.date.year != year:
            continue

        mood_trackers = [t for t in e.trackers if t.name == "mood"]
        if mood_trackers:
            # Assuming only one mood track in an entry
            r = mood_trackers[0].value
            theta = 2 * np.pi * (e.time.hour * 60 + e.time.minute) / (24 * 60)
            items.append((theta, r))

    ct = color_transform((-2, 2))

    ax.grid(True)
    ax.axis("off")

    ax.scatter([theta for theta, _ in items], [r + np.random.normal(scale=0.2) for _, r in items], c=[ct(r) for _, r in items], alpha=0.5)

    ax.set_rlim(-10, 4)
    ax.set_rmax(3)
    ax.set_rmin(-10)
    ax.set_rticks([])

    hours = list(range(0, 24, 6))
    rads = [2 * np.pi * (h / 24) for h in hours]

    if show_theta_labels:
        for r, h in zip(rads, hours):
            label = f"{h:02}:00"
            ax.text(r, 4, label, ha="center", va="center", color="#777777", fontfamily="Lora", fontstyle="italic", fontsize="medium")
    else:
        ax.vlines(rads, 1, 3, colors="#cccccc")

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    ax.text(0.16 * 2 * np.pi, 13, calendar.month_name[month], ha="right", va="top", color="#777777", fontfamily="Lora", fontstyle="italic", fontsize="medium")


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
        ax.text(i + 1.5, 7 + 0.3, day, ha="center", color="#aaaaaa", fontfamily="Lora", fontsize="x-small")

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
