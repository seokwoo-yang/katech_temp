import os
import pathlib
import shutil
import pytest
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from common.config import get_config


config = get_config()


@pytest.fixture
def setting_path():
    root = os.path.join(config.FILEBROWSER.ROOT_DIR, "temp")
    os.makedirs(os.path.join(root, "test1", "test1-1"), exist_ok=True)
    os.makedirs(os.path.join(root, "test2", "test2-1", "test2-1-1"), exist_ok=True)
    os.makedirs(os.path.join(root, "test2", "test2-2"), exist_ok=True)
    pathlib.Path(os.path.join(root, "test2", "test2-2", "test222.txt")).touch()
    os.makedirs(os.path.join(root, "test3", "test3-1"), exist_ok=True)
    pathlib.Path(os.path.join(root, "test3", "test.txt")).touch()
    pathlib.Path(os.path.join(root, "test3", "test1.txt")).touch()

    yield root

    shutil.rmtree(root)


@pytest.fixture
def setting_csv_file():
    path = os.path.join(config.FILEBROWSER.ROOT_DIR, "head_test.csv")
    with open(path, "w") as f:
        msg = """
            a,b,c
            1,2,3
            4,5,6
            6,7,4
            2,3,24
            22,,
            ,24,2
            1,2,2
            5,5,5
        """
        f.write(msg.replace(" ", "").strip())

    yield path

    pathlib.Path(path).unlink()


@pytest.fixture
def setting_link_target():
    target_dir = pathlib.Path(config.FILEBROWSER.ROOT_DIR + "/link_target_dir")
    target_dir.mkdir(exist_ok=True)

    target_file = pathlib.Path(config.FILEBROWSER.ROOT_DIR + "/link_target_file.txt")
    target_file.write_text("1234")

    yield (target_dir.resolve(), target_file.resolve())

    try:
        target_dir.unlink()
    except PermissionError:
        os.rmdir(target_dir.resolve())
    target_file.unlink()


class FilebrowserResponse:
    def __init__(self, status_code=200, content="some_content") -> None:
        self.status_code = status_code
        self.content = content


@pytest.fixture
def filebrowser_mock(monkeypatch):
    from common import filebrowser

    def mock_get_token(*args, **kwargs):
        return FilebrowserResponse(status_code=200)

    def mock_post_create_user(*args, **kwargs):
        return FilebrowserResponse(status_code=201)

    def mock_download_one(*args, **kwargs):
        return FilebrowserResponse(status_code=200)

    def mock_download_multiple(*args, **kwargs):
        return FilebrowserResponse(status_code=200)

    monkeypatch.setattr(filebrowser, "get_token", mock_get_token)
    monkeypatch.setattr(filebrowser, "post_create_user", mock_post_create_user)
    monkeypatch.setattr(filebrowser, "download_one", mock_download_one)
    monkeypatch.setattr(filebrowser, "download_multiple", mock_download_multiple)
