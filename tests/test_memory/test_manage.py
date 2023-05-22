from fukkatsu.memory.manage import get_memory, reset_memory, save_memory
from fukkatsu.memory.short import SHORT_TERM_MEMORY


def test_get_memory():
    reset_memory()
    assert get_memory() == {}


def test_reset_memory():
    assert reset_memory() == {}
