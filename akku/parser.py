import datetime
import os
import re
from glob import glob
from typing import List, Optional

import orgparse

from akku.types import Context, Entry, Person, Tracker


def parse_trackers(text: str) -> List[Tracker]:
    """
    Parser trackers in nomie format from the given body. A tracker without a
    value specification is a boolean type. For values, we only support integers
    right now. Interpretation of values are left to the consumer.
    """

    trackers = []

    for match in re.finditer(r"#([a-zA-Z\d\-]+)(\((\-?\d+)\))?", text):

        name = match.group(1)
        if match.group(3) is not None:
            value = int(match.group(3))
        else:
            value = None
        trackers.append(Tracker(name, value))

    return trackers


def parse_contexts(text: str) -> List[Context]:
    return [
        Context(match.group(1))
        for match in re.finditer(r"\+([a-zA-Z\d\-]+)", text)
    ]


def parse_people(text: str) -> List[Person]:
    return [
        Person(match.group(1))
        for match in re.finditer(r"@([a-zA-Z\d\-]+)", text)
    ]


def parse_orgzly_node(node: orgparse.node.OrgNode) -> Entry:
    """
    Parse orgzly capture style node.
    """

    if "CREATED" not in node.properties:
        raise TypeError("Invalid orgzly node")

    dts = orgparse.date.OrgDate.list_from_str(node.properties["CREATED"])

    if len(dts) != 1:
        raise TypeError("Invalid number of timestamps found")

    body = node.body.strip()

    return Entry(
        body=body,
        date=dts[0].start.date(),
        time=dts[0].start.time(),
        trackers=parse_trackers(body),
        people=parse_people(body),
        contexts=parse_contexts(body)
    )


def parse_orgzly(filepath: str) -> List[Entry]:
    """
    Parse entries from an orgzly style file where I keep entries with a heading
    'log'.
    """

    entry_heading = "log"
    root = orgparse.load(filepath)

    valid_nodes = []
    for n in root[1:]:
        if n.heading == entry_heading:
            valid_nodes.append(n)

    return [parse_orgzly_node(n) for n in valid_nodes]


def parse_list_journal_entry(text: str) -> Optional[Entry]:
    text = re.sub(r"$(\+|\-) ?", "", text).strip()

    dt_i = text.index("]")
    dt_string = text[:dt_i + 1]
    body = text[dt_i + 1:]

    dts = orgparse.date.OrgDate.list_from_str(dt_string)

    if not dts:
        return None

    dt = dts[0].start
    if isinstance(dt, datetime.datetime):
        date = dt.date()
        time = dt.time()
    else:
        date = dt
        time = None

    return Entry(
        body=body,
        date=date,
        time=time,
        trackers=parse_trackers(body),
        people=parse_people(body),
        contexts=parse_contexts(body)
    )


def parse_list_journal_heading(text: str) -> List[Entry]:
    entry_texts = []

    accum = []
    for line in text.splitlines():
        if re.match(r"(\+|\-) \[", line, flags=re.I):
            # New entry
            if accum:
                entry_texts.append("\n".join(accum))
                accum = []
        accum.append(line)

    entries = [parse_list_journal_entry(t) for t in entry_texts]
    return [e for e in entries if e]


def parse_list_journal(filepath: str) -> List[Entry]:
    """
    Lists are kept directly under headings.
    """

    root = orgparse.load(filepath)
    entries = []

    for node in root[1:]:
        # TODO: Remove this restriction
        if node.heading == "Log":
            entries.extend(parse_list_journal_heading(node.body))

    return entries


def parse_org_journal(directory: str) -> List[Entry]:
    files = glob(os.path.join(directory, "*"))

    for f in files:
        match = re.match(r"(\d{4})(\d{2})(\d{2})", f)
        if not match:
            continue
        print(match.groups())

    return []
