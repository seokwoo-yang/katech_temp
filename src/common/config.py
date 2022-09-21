from dataclasses import dataclass
from functools import lru_cache
from logging import Logger
import os
from .logger import LogFactory


@dataclass
class Filebrowser:
    ROOT_DIR: str
    CONN_URL: str


@dataclass
class Config:
    # TODO:
    """
    로깅 설정을 어떻게 할지..
    Local: stream
    test: 통합파일 ? prod: error, debug, info 등 분리
    """
    FILEBROWSER: Filebrowser


@dataclass
class LocalConfig(Config):
    FILEBROWSER: Filebrowser = Filebrowser(
        "/Users/swyang/Desktop/workspace/filebrowser_api",
        "http://192.168.101.44:8080",
    )


@dataclass
class TestConfig(Config):
    ...


@dataclass
class ProdConfig(Config):
    ...


@lru_cache
def get_config():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[os.getenv("APP_ENV", "local")]()
