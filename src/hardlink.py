import logging
import logging.config
import os
import config
import pathlib
import argparse
import json
import shutil


def get_bool(val):
    if isinstance(val, bool):
        return val
    elif val.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif val.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("must bool")


def main():
    logging.config.dictConfig(config.logging_config(f"{pathlib.Path(__file__).stem}.log"))

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
        dst_path = os.path.join(
            config.env[config.FB_ENV]["filebrowser"]["root"], args.dst_path, os.path.basename(src_path)
        )

        if os.path.exists(dst_path):
            if is_force:
                shutil.rmtree(dst_path)
            else:
                raise Exception("already exist")

        shutil.copytree(
            src=src_path,
            dst=dst_path,
            dirs_exist_ok=is_force,
            copy_function=os.link,
        )

        print({"body": dst_path})
    except Exception as e:
        logging.exception(e, exc_info=True)
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
