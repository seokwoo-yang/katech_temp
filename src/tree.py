import argparse
import logging.config
import logging
import pathlib
import sys

from common.config import get_config

CONFIG = get_config()


def walk(path):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", required=True, help="루트 디렉토리명")
    args = parser.parse_args()

    try:
        target = args.target_directory
        tree = {"body": walk(pathlib.Path(CONFIG.FILEBROWSER.ROOT_DIR) / target)}

        print(tree)
        # log.info(tree)
    except Exception as e:
        # log.exception(e, exc_info=True)
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
