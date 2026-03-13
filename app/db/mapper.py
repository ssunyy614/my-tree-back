from __future__ import annotations

from typing import Any

from app.core.config import get_settings


def underscore_to_camel(value: str) -> str:
    chunks = value.lower().split("_")
    return chunks[0] + "".join(chunk.title() for chunk in chunks[1:])


def map_row_keys(row: dict[str, Any]) -> dict[str, Any]:
    if not get_settings().mybatis.map_underscore_to_camel_case:
        return row
    return {underscore_to_camel(key): value for key, value in row.items()}
