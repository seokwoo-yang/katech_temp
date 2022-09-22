import argparse
import logging
import os
from common.filebrowser import get_token, download_one, download_multiple
from common.config import get_config

CONFIG = get_config()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src_target_path",
        required=True,
        help="다운로드 대상 파일경로(ex: /download.txt or /download_dir or /download_file,/download_dir,...)",
    )
    parser.add_argument(
        "--download_path",
        required=True,
        help="저장 위치",
    )
    parser.add_argument(
        "--type",
        required=False,
        default="zip",
        help="zip,tar,tar.gz,tar.bz2,tar.xz,tar.lz4,tar.sz",
    )

    return parser.parse_args()


def is_multi(src_path):
    if len(src_path.split(",")) > 1:
        return True
    else:
        return False


def is_dir(src_path):
    return os.path.isdir(os.path.join(CONFIG.FILEBROWSER.ROOT_DIR, src_path))


def write_to(content, download_path, type):
    path = download_path + "." + type if type else ""
    with open(path, "wb") as f:
        f.write(content)

    os.chmod(path, 755)


def main():
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    args = get_args()

    try:
        src_path = args.src_target_path
        download_path = args.download_path
        type = args.type if args.type else "zip"

        base_url = f"{CONFIG.FILEBROWSER.CONN_URL}/api"
        token = get_token(base_url).text
        if is_multi(src_path):
            response = download_multiple(base_url, token, src_path, type)
        else:
            response = download_one(base_url, token, src_path, type, is_dir(src_path))

        write_to(response.content, download_path, type)
    except Exception as e:
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
