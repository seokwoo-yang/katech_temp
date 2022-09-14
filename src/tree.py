import argparse
import logging.config
import logging
import pathlib
import sys

import config


def walk(path):
    logging.info(f"walk {path}")
    id = 0

    def nodes(p):
        nonlocal id
        lst = []
        for i in p.iterdir():
            id += 1
            if i.is_dir():
                lst.append({"text": i.name, "id": id, "nodes": nodes(i)})
            else:
                lst.append({"text": i.name, "id": id})
        return lst

    return nodes(path)


def main():
    logging.config.dictConfig(config.logging_config(f"{pathlib.Path(__file__).stem}.log"))

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", required=True, help="루트 디렉토리명")
    args = parser.parse_args()

    try:
        target = args.target_directory
        tree = {"body": walk(pathlib.Path(config.env["filebrowser"]["root"]) / target)}

        print(tree)
    except Exception as e:
        logging.exception(e)
        print({"body": []})


if __name__ == "__main__":
    main()
