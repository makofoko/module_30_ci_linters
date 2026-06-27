import pytest
from src import main


def test_main_runs():
    result = main.run()
    assert result is True

