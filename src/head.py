import logging.config
import logging
import pathlib
import sys
import argparse

import pandas as pd

from common.config import get_config

CONFIG = get_config()


def head(path, lines):
    df = pd.read_excel(path, header=None) if path.suffix in ["xls", "xlsx"] else pd.read_csv(path, header=None)
    return df[:lines].values.tolist()


def main():
    parser = argparse.ArgumentParser(description="파일 미리보기")
    parser.add_argument("--target_file_directory", required=True, help="미리보기 대상 파일")
    parser.add_argument("--rows", required=True, help="라인 수")
    args = parser.parse_args()

    try:
        target = args.target_file_directory
        lines = args.rows
        rows = {"body": head(pathlib.Path(CONFIG.FILEBROWSER.ROOT_DIR) / target, int(lines))}

        print(rows)
        # logging.info(rows)
    except Exception as e:
        # logging.exception(e, exc_info=True)
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()

    # import json
    # rows = head(pathlib.Path("head.csv"), 5)
    # print(json.dumps(rows, indent=2))
