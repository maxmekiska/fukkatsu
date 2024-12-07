import hashlib
import sqlite3
from typing import Optional

import lz4.frame


class ShortMemory:
    """
    A class for managing fixes and solutions in a SQLite database.
    """

    _connection: Optional[sqlite3.Connection] = None

    def __init__(self, db_name: str = ":memory:") -> None:
        """
        Initializes the database connection and ensures the fixes table exists.
        :param db_name: Name of the SQLite database file or ':memory:' for an in-memory database.
        """
        if ShortMemory._connection is None:
            ShortMemory._connection = sqlite3.connect(db_name)
        self._cursor = ShortMemory._connection.cursor()
        self._initialize_table()

    def _initialize_table(self) -> None:
        """Creates the fixes table if it does not exist."""
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fixes (
                hash TEXT PRIMARY KEY,
                solution BLOB
            )
        """
        )
        if ShortMemory._connection:
            ShortMemory._connection.commit()

    @staticmethod
    def _hash_error_trace(error_trace: str) -> str:
        """
        Generates a SHA-256 hash for the given error trace.
        :param error_trace: The error trace to hash.
        :return: A SHA-256 hash as a hexadecimal string.
        """
        return hashlib.sha256(error_trace.encode()).hexdigest()

    @staticmethod
    def _compress_code(code: str) -> bytes:
        """
        Compresses the given Python code using LZ4.
        :param code: The Python code as a string.
        :return: The compressed code as bytes.
        """
        return lz4.frame.compress(code.encode())

    @staticmethod
    def _decompress_code(code: bytes) -> str:
        """
        Decompresses the given Python code using LZ4.
        :param code: The compressed Python code as bytes.
        :return: The original code as a string.
        """
        return lz4.frame.decompress(code).decode()

    def exists(self, error_trace: str) -> bool:
        """Check if a trace exists in the database."""
        hash_value = self._hash_error_trace(error_trace)
        self._cursor.execute("SELECT solution FROM fixes WHERE hash = ?", (hash_value,))
        return self._cursor.fetchone() is not None

    def store_fix(self, error_trace: str, solution: str) -> None:
        """
        Inserts or updates an error trace and its solution in the database.
        :param error_trace: The error trace to store.
        :param solution: The corresponding solution.
        """
        compressed_solution = self._compress_code(solution)
        hash_value = self._hash_error_trace(error_trace)
        self._cursor.execute(
            """
            INSERT INTO fixes (hash, solution)
            VALUES (?, ?)
            ON CONFLICT(hash) DO UPDATE SET solution = excluded.solution
        """,
            (hash_value, compressed_solution),
        )
        if ShortMemory._connection:
            ShortMemory._connection.commit()

    def get_fix(self, error_trace: str) -> Optional[str]:
        """
        Retrieves the solution for a given error trace.
        :param error_trace: The error trace to retrieve the solution for.
        :return: The solution if found, otherwise None.
        """
        hash_value = self._hash_error_trace(error_trace)
        self._cursor.execute("SELECT solution FROM fixes WHERE hash = ?", (hash_value,))
        result = self._cursor.fetchone()

        if result:
            compressed_solution = result[0]
            return self._decompress_code(compressed_solution)
        else:
            return None

    def show_table(self) -> list[tuple[str, str]]:
        """
        Retrieves all rows from the fixes table for debugging or inspection.
        :return: A list of tuples containing the hash and solution.
        """
        self._cursor.execute("SELECT * FROM fixes")
        return self._cursor.fetchall()

    def delete(self) -> None:
        """
        Deletes all records from the table.
        """
        self._cursor.execute("DELETE FROM fixes")
        if ShortMemory._connection:
            ShortMemory._connection.commit()

    def __del__(self) -> None:
        """Closes the database connection when the object is destroyed."""
        if ShortMemory._connection:
            ShortMemory._connection.close()
            ShortMemory._connection = None
