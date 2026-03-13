from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class AppConfig:
    name: str


@dataclass(frozen=True)
class ServerConfig:
    host: str
    port: int
    reload: bool


@dataclass(frozen=True)
class OracleConfig:
    host: str
    port: int
    sid: str
    username: str
    password: str
    encoding: str


@dataclass(frozen=True)
class MyBatisConfig:
    map_underscore_to_camel_case: bool


@dataclass(frozen=True)
class Settings:
    app: AppConfig
    server: ServerConfig
    oracle: OracleConfig
    mybatis: MyBatisConfig


def _load_yaml() -> dict[str, Any]:
    config_path = Path(__file__).resolve().parents[2] / "application.yml"
    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    raw = _load_yaml()
    app = raw.get("app", {})
    server = raw.get("server", {})
    database = raw.get("database", {})
    oracle = database.get("oracle", {})
    mybatis = raw.get("mybatis", {})

    return Settings(
        app=AppConfig(
            name=app.get("name", "my-tree-back"),
        ),
        server=ServerConfig(
            host=server.get("host", "0.0.0.0"),
            port=int(server.get("port", 8081)),
            reload=bool(server.get("reload", False)),
        ),
        oracle=OracleConfig(
            host=oracle.get("host", "localhost"),
            port=int(oracle.get("port", 1521)),
            sid=oracle.get("sid", "xe"),
            username=oracle.get("username", "lghr"),
            password=str(oracle.get("password", "12345")),
            encoding=oracle.get("encoding", "UTF-8"),
        ),
        mybatis=MyBatisConfig(
            map_underscore_to_camel_case=bool(
                mybatis.get("map-underscore-to-camel-case", True)
            ),
        ),
    )
