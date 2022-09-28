import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import pathlib
from common.config import get_config
from tree import walk

config = get_config()


def test_tree(setting_path):
    assert walk(pathlib.Path(setting_path)) == [
        {"text": "test1", "id": 1, "nodes": [{"text": "test1-1", "id": 2}]},
        {
            "text": "test3",
            "id": 3,
            "nodes": [{"text": "test1.txt", "id": 4}, {"text": "test3-1", "id": 5}, {"text": "test.txt", "id": 6}],
        },
        {
            "text": "test2",
            "id": 7,
            "nodes": [
                {"text": "test2-1", "id": 8, "nodes": [{"text": "test2-1-1", "id": 9}]},
                {"text": "test2-2", "id": 10, "nodes": [{"text": "test222.txt", "id": 11}]},
            ],
        },
    ]
