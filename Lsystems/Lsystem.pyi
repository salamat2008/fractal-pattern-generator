from __future__ import annotations

from typing import Iterable, overload


class LSystem:
    """
    ___
    """
    
    @overload
    def __init__(self, other: 'LSystem' | None = ...) -> None: ...
    
    @overload
    def __init__(
            self,
            rule: Iterable[str] | dict[str, str] | str | None = ...,
            keywords: Iterable[str] | Iterable[Iterable[str]] | None = ...,
    ) -> None: ...
