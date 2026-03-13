from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

import oracledb

from app.core.config import get_settings


def build_dsn() -> str:
    settings = get_settings()
    return oracledb.makedsn(
        host=settings.oracle.host,
        port=settings.oracle.port,
        sid=settings.oracle.sid,
    )


@lru_cache(maxsize=1)
def get_pool() -> oracledb.ConnectionPool:
    settings = get_settings()
    return oracledb.create_pool(
        user=settings.oracle.username,
        password=settings.oracle.password,
        dsn=build_dsn(),
        min=1,
        max=5,
        increment=1,
    )


@contextmanager
def get_connection() -> Iterator[oracledb.Connection]:
    connection = get_pool().acquire()
    try:
        yield connection
    finally:
        connection.close()
