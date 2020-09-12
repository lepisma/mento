import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Tracker:
    name: str
    value: float = None


@dataclass
class Person:
    name: str


@dataclass
class Context:
    name: str


@dataclass
class Entry:
    body: str
    time: datetime.datetime
    trackers: List[Tracker] = None
    people: List[Person] = None
    contexts: List[Context] = None
