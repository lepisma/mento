import datetime
import hashlib
import os
from glob import glob

from akku.types import Entry


def file_hash(filepath: str) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as fp:
        h.update(fp.read())
    return h.hexdigest()


def directory_hash(directory: str) -> str:
    files = glob(os.path.join(directory, "**/*"), recursive=True)

    h = hashlib.md5()
    for filepath in files:
        h.update(bytes(filepath, "utf-8"))
        with open(filepath, "rb") as fp:
            h.update(fp.read())

    return h.hexdigest()


def entry_dt(entry: Entry) -> datetime.datetime:
    return datetime.datetime.combine(entry.date, entry.time or datetime.time.min)
