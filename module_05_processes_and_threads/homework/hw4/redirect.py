import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, *, stdout: IO = None, stderr: IO = None) -> None:
        self._new_stdout = stdout
        self._new_stderr = stderr
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        if self._new_stdout is not None:
            self._old_stdout = sys.stdout
            sys.stdout = self._new_stdout
        if self._new_stderr is not None:
            self._old_stderr = sys.stderr
            sys.stderr = self._new_stderr
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is not None and self._new_stderr is not None:
            self._new_stderr.write("".join(traceback.format_exception(exc_type, exc_val, exc_tb)))
            self._new_stderr.flush()

        if self._old_stdout is not None:
            sys.stdout = self._old_stdout
        if self._old_stderr is not None:
            sys.stderr = self._old_stderr

        return None