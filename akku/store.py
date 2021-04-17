import sqlite3
from typing import List

from akku.parser import parse_source
from akku.types import Entry, Source, SourceType, entry_dumps, entry_loads
from akku.util import directory_hash, file_hash


def calculate_cache_state(source: Source) -> str:
    if source.source_type == SourceType.ORGZLY:
        return file_hash(source.path)
    elif source.source_type == SourceType.ORG_LIST:
        return file_hash(source.path)
    elif source.source_type == SourceType.ORG_JOURNAL:
        return directory_hash(source.path)
    else:
        raise TypeError("Wrong source type")


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

    def refresh(self, force=False):
        cur = self.con.cursor()

        rows = cur.execute("SELECT id, type, path, config, cache_state FROM sources").fetchall()

        for row in rows:
            s_id = row[0]
            source = Source(SourceType[row[1]], row[2], row[3])

            stored_cache_state = row[4]
            current_cache_state = calculate_cache_state(source)

            if force or (stored_cache_state != current_cache_state):
                print(f":: Refreshing source: {source.path}")
                cur.execute("DELETE FROM entries WHERE source_id = ?", (s_id, ))
                entries = parse_source(source)
                cur.executemany(
                    "INSERT INTO entries (data, source_id) VALUES (?, ?)",
                    [(entry_dumps(ent), s_id) for ent in entries]
                )

            cur.execute("UPDATE sources SET cache_state = ? WHERE id = ?", (current_cache_state, s_id))

        self.con.commit()

    def _init_db(self):
        cur = self.con.cursor()

        cur.execute("CREATE TABLE sources (id INTEGER PRIMARY KEY, type, path, config, cache_state)")
        cur.execute("CREATE TABLE entries (id INTEGER PRIMARY KEY, data, source_id, FOREIGN KEY (source_id) REFERENCES sources (id))")

        self.con.commit()
