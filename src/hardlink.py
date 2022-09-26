import os
import argparse
import pathlib
import shutil

from common.config import get_config

CONFIG = get_config()


def get_bool(val):
    if isinstance(val, bool):
        return val
    elif val.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif val.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("must bool")


def hardlink(src_path, dst_path, is_force):
    if os.path.exists(dst_path):
        if is_force:
            shutil.rmtree(dst_path)
        else:
            raise Exception("already exist")

    if os.path.isfile(src_path):
        os.link(src_path, dst_path)
    else:
        shutil.copytree(
            src=src_path,
            dst=dst_path,
            dirs_exist_ok=is_force,
            copy_function=os.link,
        )


def main():
    parser = argparse.ArgumentParser(description="마이디스크 저장(관심데이터or찜데이터)")
    parser.add_argument("--src_path", required=True, help="복사 대상(파일 또는 디렉터리)")
    parser.add_argument(
        "--force",
        default=False,
        required=False,
        type=get_bool,
        help="중복시 덮어쓸지, 넘어갈지(yes|no, true|false, t|f, y|n, 1|0)",
    )
    parser.add_argument("--dst_path", required=True, help="복사할 위치 기본 dir(계정명 or 계정/찜dir or dataset?)")
    args = parser.parse_args()

    try:
        is_force = args.force
        src_path = args.src_path
        base_dst = os.path.join(CONFIG.FILEBROWSER.ROOT_DIR, args.dst_path)
        if pathlib.Path(base_dst).is_file():
            dst_path = os.path.join(base_dst, os.path.basename(src_path))
        else:
            dst_path = base_dst

        hardlink(src_path, dst_path, is_force)

        print({"body": dst_path})
    except Exception as e:
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
