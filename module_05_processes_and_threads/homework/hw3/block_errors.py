from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection[Type[BaseException]]) -> None:
        self.errors = tuple(errors)

    def __enter__(self) -> None:
        return None

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is None:
            return None
        if issubclass(exc_type, self.errors):
            return True

        return None