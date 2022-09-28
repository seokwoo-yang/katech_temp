import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import pathlib
from head import head, main


def test_head(setting_csv_file):
    with open(setting_csv_file, "r") as f:
        lines = f.readlines()

    for i in range(0, 10):
        assert head(pathlib.Path(setting_csv_file), i) == [line.strip().split(",") for line in lines[:i]]


def test_head_main(monkeypatch):
    """
    TODO: monkeypatch 활용하여 mocking?
    """

    monkeypatch.setattr("sys.argv", ["head.py", "--target_file_directory", "head_test.csv", "--rows", "10"])
    main()

    monkeypatch.setattr("sys.argv", ["head.py", "--target_file_directory", "head_test.csv", "--rows", "a"])
    main()
