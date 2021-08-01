import pytest
from mento.parser import (parse_contexts, parse_list_journal_heading,
                          parse_people, parse_trackers)
from mento.types import Context, Person, Tracker


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


def test_list_journal_parsing():
    text = """+ [2021-03-12 Fri 19:34] #mood(0) hello
  multiline stuff.
+ [2021-03-12 Fri 19:15] #mood(-1)
+ [2021-03-12 Fri 19:00] #mood(-2)

"""

    assert len(parse_list_journal_heading(text)) == 3
