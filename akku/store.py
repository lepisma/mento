import sqlite3
from typing import List

from akku.parser import parse_source
from akku.types import Entry, Source, SourceType, entry_dumps, entry_loads


class SQLiteStore:
    """
    Basic SQLite database without much schema for storing sources and entries.
    """

    def __init__(self, path: str):
        self.con = sqlite3.connect(path)

        if not self.con.execute("SELECT name FROM sqlite_master").fetchall():
            self._init_db()

    @property
    def entries(self) -> List[Entry]:
        cur = self.con.cursor()
        return [entry_loads(it[0]) for it in cur.execute("SELECT data FROM entries")]

    def refresh(self):
        # TODO: Allow unforced refreshes
        cur = self.con.cursor()

        # Deleting all items and re-parsing everything
        cur.execute("DELETE FROM entries")

        sources = {}
        for row in cur.execute("SELECT id, type, path, config FROM sources"):
            sources[row[0]] = Source(SourceType[row[1]], row[2], row[3])

        for s_id, source in sources.items():
            entries = parse_source(source)
            rows = [(entry_dumps(ent), s_id) for ent in entries]
            cur.executemany("INSERT INTO entries (data, source_id) VALUES (?, ?)", rows)

        self.con.commit()

    def _init_db(self):
        cur = self.con.cursor()

        cur.execute("CREATE TABLE sources (id INTEGER PRIMARY KEY, type, path, config, cache_state)")
        cur.execute("CREATE TABLE entries (id INTEGER PRIMARY KEY, data, source_id, FOREIGN KEY (source_id) REFERENCES sources (id))")

        self.con.commit()
