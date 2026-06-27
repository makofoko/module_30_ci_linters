import pytest
from src import main  # type: ignore


def test_main_runs():
    result = main.run()
    assert result is True