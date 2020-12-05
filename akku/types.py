import datetime
from dataclasses import dataclass
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
