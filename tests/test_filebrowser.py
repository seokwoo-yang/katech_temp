import sys
import os
from common.config import get_config

from common import filebrowser

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))


config = get_config()


def test_get_token(filebrowser_mock):
    assert filebrowser.get_token("http://fakeurl").content == "some_content"


def test_post_create_user(filebrowser_mock):
    assert (
        filebrowser.post_create_user(
            base_url="http://fakeurl",
            token="token",
            scope="scope",
            username="username",
            password="password",
        ).status_code
        == 201
    )


def test_download_one(filebrowser_mock):
    ...


def test_download_multiple(filebrowser_mock):
    ...
