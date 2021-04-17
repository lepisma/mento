import datetime
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
