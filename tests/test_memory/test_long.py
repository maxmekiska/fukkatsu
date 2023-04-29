import pytest

from fukkatsu.memory.long import LONG_TERM_MEMORY


def test_long():
    assert LONG_TERM_MEMORY == {}
