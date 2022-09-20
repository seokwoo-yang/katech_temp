import argparse
import pathlib

from common.config import get_config

CONFIG = get_config()


def walk(path):
    id = 0

    def nodes(p):
        nonlocal id
        lst = []
        for i in p.iterdir():
            id += 1
            data = {"text": i.name, "id": id}
            if i.is_dir():
                node = nodes(i)
                if node:
                    data["nodes"] = node

            lst.append(data)
        return lst

    return nodes(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", required=True, help="루트 디렉토리명")
    args = parser.parse_args()

    try:
        print(CONFIG.BASE_DIR)
        target = args.target_directory
        tree = {"body": walk(pathlib.Path(CONFIG.FILEBROWSER.ROOT_DIR) / target)}

        print(tree)
    except Exception as e:
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
