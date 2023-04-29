import pytest

from fukkatsu.memory.short import SHORT_TERM_MEMORY


def test_short():
    assert SHORT_TERM_MEMORY == {}
