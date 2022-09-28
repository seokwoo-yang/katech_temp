import pathlib
import sys
import os
import stat

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from hardlink import hardlink
from common.config import get_config

config = get_config()


def test_hardlink(setting_link_target, monkeypatch):
    # monkeypatch.setattr("sys.argv", "hardlink.py", "--src_path")
    target_dir, target_file = setting_link_target

    try:
        dst_path = config.FILEBROWSER.ROOT_DIR + "/test_dir"
        hardlink(target_dir, dst_path, True)

        assert pathlib.Path(dst_path).exists()
    finally:
        if os.path.isdir(dst_path):
            os.rmdir(dst_path)

    try:
        dst_path = config.FILEBROWSER.ROOT_DIR + "/test_file"
        hardlink(target_file, dst_path, True)

        assert pathlib.Path(dst_path).exists()
        with open(target_file, "r") as f:
            with open(dst_path, "r") as ff:
                assert f.readline() == ff.readline()

        assert os.stat(target_file)[stat.ST_INO] == os.stat(dst_path)[stat.ST_INO]
    finally:
        if os.path.isfile(dst_path):
            os.unlink(dst_path)
