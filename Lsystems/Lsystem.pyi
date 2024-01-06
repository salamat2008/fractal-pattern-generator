from __future__ import annotations

from typing import Generator, Iterable, overload


class LSystem(object):
    __rules: dict[str, str]
    __keywords: tuple[tuple[str, ...], ...]
    
    @overload
    def __init__(
            self, rules: Iterable[str] | dict[str, str] | str | None = ...,
            keywords: Iterable[str] | Iterable[Iterable[str]] | None = ...
    ) -> None: ...
    
    @overload
    def __init__(self, other: LSystem | None = ...) -> None: ...
    
    def __init__(self): ...
    
    @property
    def rules(self) -> dict[str, str]: ...
    
    @rules.setter
    def rules(self, rules: Iterable[str] | dict[str, str] | str) -> None: ...
    
    @property
    def keywords(self) -> tuple[tuple[str, ...], ...]: ...
    
    @keywords.setter
    def keywords(self, keywords: Iterable[str] | Iterable[Iterable[str]]) -> None: ...
    
    def generate_action_string(
            self,
            string: str,
            number_of_iterations: int,
            my_memory_endless: bool = False
    ) -> tuple[tuple[str, int]]: ...
    
    @staticmethod
    def clear_database(): ...
    
    def formatting(self, string: str) -> Generator[tuple[str, int], None, None]: ...
    
    def multiplication(self, argument: str) -> str: ...
