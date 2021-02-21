import datetime
import statistics
from typing import Any, Callable, Dict, List, Optional

import pandas as pd
from pydash import py_

from akku.types import Entry


def aggregate_mean_mood(entries: List[Entry]) -> Optional[float]:
    trackers = py_.flatten([e.trackers for e in entries])
    mood_trackers = [t for t in trackers if t.name == "mood"]

    if mood_trackers:
        return statistics.mean([t.value for t in mood_trackers])
    return None


def aggregate_number_of_mentions(entries: List[Entry], name: str) -> int:
    people = py_.flatten([e.people for e in entries])
    mentions = [p for p in people if p.name == name]

    return len(mentions)


def aggregate_by_date(entries: List[Entry], aggregate_fn: Callable[[List[Entry]], Any]) -> Dict[datetime.date, Any]:
    return {
        date: aggregate_fn(entries)
        for date, entries in py_.group_by(entries, lambda e: e.date).items()
    }
