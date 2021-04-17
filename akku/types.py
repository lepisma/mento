import dataclasses
import datetime
import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class Tracker:
    name: str
    value: Optional[int] = None


@dataclass
class Person:
    name: str


@dataclass
class Context:
    name: str


@dataclass
class Entry:
    body: str
    date: datetime.date
    time: Optional[datetime.time] = None
    trackers: Optional[List[Tracker]] = None
    people: Optional[List[Person]] = None
    contexts: Optional[List[Context]] = None


class SourceType(Enum):
    """
    Various sources of entries.
    """

    ORGZLY = 1
    ORG_LIST = 2
    ORG_JOURNAL = 3


@dataclass
class Source:
    source_type: SourceType
    path: str
    config: str


def entry_dumps(ent: Entry) -> str:
    def _enc(o):
        if isinstance(o, (datetime.date, datetime.time)):
            return o.isoformat()

    return json.dumps(
        dataclasses.asdict(ent),
        default=_enc
    )


def entry_loads(text: str) -> Entry:
    d = json.loads(text)

    d["date"] = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
    if d["time"]:
        d["time"] = datetime.datetime.strptime(d["time"], "%H:%M:%S").time()

    # HACK: Nested dataclasses
    if d["trackers"]:
        d["trackers"] = [Tracker(**t) for t in d["trackers"]]

    if d["people"]:
        d["people"] = [Person(**t) for t in d["people"]]

    if d["contexts"]:
        d["contexts"] = [Context(**t) for t in d["contexts"]]

    return Entry(**d)
