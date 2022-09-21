from dataclasses import dataclass
from functools import lru_cache
from logging import Logger
import os
import logging

from common.logger import LogFactory


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
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    FILEBROWSER: Filebrowser = None


@dataclass
class LocalConfig(Config):
    LOG: Logger = LogFactory.get_stream_logger()
    FILEBROWSER: Filebrowser = Filebrowser(
        "/Users/swyang/Desktop/workspace/filebrowser_api",
        "http://192.168.101.44:8080",
    )


@dataclass
class TestConfig(Config):
    LOG_PATH: str = os.path.join(Config.BASE_DIR, "../../log")
    LOG_LEVEL: int = logging.INFO
    LOG: Logger = LogFactory.get_file_logger(path=LOG_PATH, level=LOG_LEVEL)
    FILEBROWSER: Filebrowser = Filebrowser(
        "/home/deep/workspace/ysw/katech/filebrowser/swyang_test_database",
        "http://localhost:8080",
    )


@dataclass
class ProdConfig(Config):
    ...


# @lru_cache
def get_config():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[os.getenv("APP_ENV", "test")]()
