import pytest
from src import main

from module_30_ci_linters import main


def test_main_runs():
    result = main.run()
    assert result is True
