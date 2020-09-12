from typing import List

import pandas as pd

import calmap
from akku.types import Entry


def plot_entries(entries: List[Entry]):
    """
    TODO: More detailed plots
    """

    series = pd.Series([1 for _ in entries], index=pd.DatetimeIndex([e.date for e in entries]))
    series = series.groupby(level=0).sum()
    calmap.calendarplot(series)
