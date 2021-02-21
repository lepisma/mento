import datetime

from akku.types import Entry


def entry_dt(entry: Entry) -> datetime.datetime:
    return datetime.datetime.combine(entry.date, entry.time or datetime.time.min)
