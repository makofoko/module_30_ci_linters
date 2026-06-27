import pytest

from module_30_ci_linters.materials.gitlab_ci import main

def test_main_runs():
    result = main.run()
    assert result is True