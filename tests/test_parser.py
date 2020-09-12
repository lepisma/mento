import pytest

from akku.parser import parse_contexts, parse_people, parse_trackers
from akku.types import Context, Person, Tracker


@pytest.mark.parametrize("text, output", [
    ("hello", []),
    ("feeling very rejected today #mood(-2)", [Tracker("mood", -2)]),
    ("got an #attack today", [Tracker("attack")])
])
def test_parse_trackers(text, output):
    assert parse_trackers(text) == output


@pytest.mark.parametrize("text, output", [
    ("hello", []),
    ("i talked to @person-a today", [Person("person-a")]),
    ("@a got annoyed on me. @b wasn't around and i felt sad.", [Person("a"), Person("b")])
])
def test_parse_people(text, output):
    assert parse_people(text) == output


@pytest.mark.parametrize("text, output", [
    ("hello", []),
    ("today this happened ... +vacation", [Context("vacation")]),
    ("i wasn't happy at +work today. i also got +sick.", [Context("work"), Context("sick")])
])
def test_parse_contexts(text, output):
    assert parse_contexts(text) == output
