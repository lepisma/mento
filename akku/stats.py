import datetime
import statistics
from typing import Any, Callable, Dict, List, Optional

from pydash import py_
from textblob import TextBlob

from akku.types import Entry


def aggregate_mean_mood(entries: List[Entry]) -> Optional[float]:
    trackers = py_.flatten([e.trackers for e in entries])
    mood_trackers = [t for t in trackers if t.name == "mood"]

    if mood_trackers:
        return statistics.mean([t.value for t in mood_trackers])
    return None


def aggregate_mean_polarity(entries: List[Entry]) -> float:
    return statistics.mean([TextBlob(ent.body).sentiment.polarity for ent in entries])


def aggregate_mentions(entries: List[Entry]) -> int:
    return len(py_.flatten([e.people for e in entries]))


def aggregate_by_date(entries: List[Entry], aggregate_fn: Callable[[List[Entry]], Any]) -> Dict[datetime.date, Any]:
    return {
        date: aggregate_fn(entries)
        for date, entries in py_.group_by(entries, lambda e: e.date).items()
    }
