import re
from typing import List

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
