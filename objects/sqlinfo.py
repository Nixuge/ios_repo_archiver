from dataclasses import dataclass
from sqlite3 import Connection, Cursor


@dataclass
class SQLInfo:
    connection: Connection
    cursor: Cursor