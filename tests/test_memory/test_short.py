import pytest

from fukkatsu.memory.short import ShortMemory


@pytest.fixture
def memory_db() -> ShortMemory:
    """
    Fixture to create a fresh ShortMemory instance for each test.
    Uses an in-memory database to avoid persistence between tests.
    """
    return ShortMemory(db_name=":memory:")


def test_initialization(memory_db: ShortMemory):
    """
    Test that the ShortMemory instance is created successfully
    and the fixes table exists.
    """
    # Verify cursor and connection are set up
    assert memory_db._cursor is not None

    # Check that the table exists
    memory_db._cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='fixes'"
    )
    assert memory_db._cursor.fetchone() is not None


def test_hash_error_trace():
    """
    Test the static method for generating hash values.
    """
    error_trace = "Some error message"
    hash_value = ShortMemory._hash_error_trace(error_trace)

    assert len(hash_value) == 64
    assert all(c in "0123456789abcdef" for c in hash_value)


def test_compression_and_decompression():
    """
    Test LZ4 compression and decompression methods.
    """
    original_code = "def example_function():\n    return 'Hello, World!'"

    compressed_code = ShortMemory._compress_code(original_code)
    assert isinstance(compressed_code, bytes)

    decompressed_code = ShortMemory._decompress_code(compressed_code)
    assert decompressed_code == original_code


def test_store_and_retrieve_fix(memory_db: ShortMemory):
    """
    Test storing and retrieving a solution for an error trace.
    """
    error_trace = "TypeError: Cannot add string to integer"
    solution = "def fix_type_error(a, b):\n    return int(a) + int(b)"

    memory_db.store_fix(error_trace, solution)

    assert memory_db.exists(error_trace) is True

    retrieved_solution = memory_db.get_fix(error_trace)
    assert retrieved_solution == solution


def test_update_existing_fix(memory_db: ShortMemory):
    """
    Test updating an existing fix with a new solution.
    """
    error_trace = "ValueError: Invalid input"
    initial_solution = "def first_solution():\n    pass"
    updated_solution = "def updated_solution():\n    return True"

    memory_db.store_fix(error_trace, initial_solution)

    memory_db.store_fix(error_trace, updated_solution)

    retrieved_solution = memory_db.get_fix(error_trace)
    assert retrieved_solution == updated_solution


def test_non_existent_fix(memory_db: ShortMemory):
    """
    Test retrieving a non-existent fix.
    """
    error_trace = "Non-existent error trace"

    assert memory_db.exists(error_trace) is False
    assert memory_db.get_fix(error_trace) is None


def test_show_table(memory_db: ShortMemory):
    """
    Test showing the contents of the fixes table.
    """
    fixes = [
        ("Error1", "def solution1():\n    pass"),
        ("Error2", "def solution2():\n    return True"),
    ]

    for error_trace, solution in fixes:
        memory_db.store_fix(error_trace, solution)

    table_contents = memory_db.show_table()

    assert len(table_contents) == 2

    for row in table_contents:
        assert len(row[0]) == 64  # hash length
        assert isinstance(row[1], bytes)  # compressed solution


def test_delete_table(memory_db: ShortMemory):
    """
    Test deleting all records from the table.
    """
    memory_db.store_fix("Error1", "def solution1():\n    pass")
    memory_db.store_fix("Error2", "def solution2():\n    return True")

    assert len(memory_db.show_table()) > 0

    memory_db.delete()

    assert len(memory_db.show_table()) == 0


def test_multiple_instances():
    """
    Test that multiple instances share the same connection.
    """
    db1 = ShortMemory(":memory:")
    db2 = ShortMemory(":memory:")

    error_trace = "Test Error"
    solution = "def test_solution():\n    pass"
    db1.store_fix(error_trace, solution)

    assert db2.exists(error_trace) is True
    assert db2.get_fix(error_trace) == solution
