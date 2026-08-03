# codex_index.py

import sqlite3
from pathlib import Path


class CodexIndex:
    def __init__(self, db_path=".codex/index.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        self._initialize()

    def _initialize(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            hash TEXT,
            language TEXT,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            kind TEXT,
            line INTEGER,
            FOREIGN KEY (file_id)
                REFERENCES files(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol_id INTEGER NOT NULL,
            file_id INTEGER NOT NULL,
            line INTEGER,
            FOREIGN KEY (symbol_id)
                REFERENCES symbols(id)
                ON DELETE CASCADE,
            FOREIGN KEY (file_id)
                REFERENCES files(id)
                ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_files_path
            ON files(path);

        CREATE INDEX IF NOT EXISTS idx_symbols_name
            ON symbols(name);
        """)

        self.conn.commit()

    def add_file(self, path, file_hash=None, language=None):
        self.conn.execute(
            """
            INSERT INTO files (path, hash, language)
            VALUES (?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                hash = excluded.hash,
                language = excluded.language,
                indexed_at = CURRENT_TIMESTAMP
            """,
            (str(path), file_hash, language),
        )

        self.conn.commit()

    def add_symbol(self, file_path, name, kind, line):
        file_row = self.conn.execute(
            "SELECT id FROM files WHERE path = ?",
            (str(file_path),),
        ).fetchone()

        if not file_row:
            raise ValueError(f"File is not indexed: {file_path}")

        self.conn.execute(
            """
            INSERT INTO symbols
                (file_id, name, kind, line)
            VALUES (?, ?, ?, ?)
            """,
            (file_row["id"], name, kind, line),
        )

        self.conn.commit()

    def search_symbol(self, name):
        return self.conn.execute(
            """
            SELECT
                symbols.name,
                symbols.kind,
                symbols.line,
                files.path
            FROM symbols
            JOIN files
                ON symbols.file_id = files.id
            WHERE symbols.name LIKE ?
            ORDER BY files.path, symbols.line
            """,
            (f"%{name}%",),
        ).fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    index = CodexIndex()

    index.add_file(
        "src/main.py",
        file_hash="abc123",
        language="python",
    )

    index.add_symbol(
        "src/main.py",
        "CodexIndex",
        "class",
        7,
    )

    for result in index.search_symbol("Codex"):
        print(dict(result))

    index.close()