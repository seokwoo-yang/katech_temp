import logging.config
import logging
import pathlib
import sys
import argparse

import pandas as pd

import config


def head(path, lines):
    logging.info(f"head {path}, {lines}")
    df = pd.read_excel(path, header=None) if path.suffix in ["xls", "xlsx"] else pd.read_csv(path, header=None)
    return df[:lines].values.tolist()
    # return "\n".join([",".join(str) for str in df[:lines].values.tolist()])


def main():
    logging.config.dictConfig(config.logging_config(f"{pathlib.Path(__file__).stem}.log"))

    parser = argparse.ArgumentParser(description="파일 미리보기")
    parser.add_argument("--target_file_directory", required=True, help="미리보기 대상 파일")
    parser.add_argument("--rows", required=True, help="라인 수")
    args = parser.parse_args()

    try:
        target = args.target_file_directory
        lines = args.rows
        rows = {"body": head(pathlib.Path(config.env["filebrowser"]["root"]) / target, int(lines))}

        print(rows)
    except Exception as e:
        logging.exception(e)
        print({"body": []})


if __name__ == "__main__":
    main()

    # import json
    # rows = head(pathlib.Path("head.csv"), 5)
    # print(json.dumps(rows, indent=2))
