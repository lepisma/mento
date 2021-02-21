import datetime
import math
import statistics
from typing import Dict, List

import pandas as pd
from pydash import py_

from akku.types import Entry


def summarize_number_of_entries(entries: List[Entry]):
    current_year = datetime.datetime.now().year
    filtered = [e for e in entries if e.date.year == current_year]

    df = []
    for date, entries in py_.group_by(filtered, lambda e: e.date).items():
        df.append({
            "day": date.timetuple().tm_yday,
            "value": len(entries)
        })

    return pd.DataFrame(df)


def summarize_number_of_mentions(entries: List[Entry], name: str):
    """
    Number of mention of a person. Matches by using nomie thing only. Regex
    match will give more real stats for older dates.
    """

    current_year = datetime.datetime.now().year
    filtered = [e for e in entries if e.date.year == current_year]

    df = []
    for date, entries in py_.group_by(filtered, lambda e: e.date).items():
        people = py_.flatten([e.people for e in entries])
        mentions = [p for p in people if p.name == name]

        if mentions:
            df.append({
                "day": date.timetuple().tm_yday,
                "value": len(mentions)
            })

    return pd.DataFrame(df)


def aggregate_mood(entries: List[Entry]) -> Dict[datetime.date, float]:
    output = {}
    for date, entries in py_.group_by(entries, lambda e: e.date).items():
        trackers = py_.flatten([e.trackers for e in entries])
        mood_trackers = [t for t in trackers if t.name == "mood"]

        if mood_trackers:
            output[date] = statistics.mean([t.value for t in mood_trackers])

    return output
