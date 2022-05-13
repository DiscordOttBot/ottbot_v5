import typing as t
from .prepared_stmt import PreparedStatement
from .protocol import Record

class PoolConnectionProxy:
    """Proxy class for a connection."""

    async def prepare(
        self, query: str, *, timeout: float | None = ..., record_class: Record | None = ...
    ) -> PreparedStatement: ...
    async def execute(self, query: str, *args: t.Any, timeout: float | None = ...) -> str: ...
