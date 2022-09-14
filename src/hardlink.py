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
    print(os.path.abspath(__file__))
    logging.config.dictConfig(config.logging_config(f"{pathlib.Path(__file__).stem}.log"))

    parser = argparse.ArgumentParser(description="마이디스크 저장(관심데이터or찜데이터)")
    parser.add_argument("--target_path", required=True, help="복사 대상(파일 또는 디렉터리)")
    parser.add_argument(
        "--force",
        default=False,
        required=False,
        type=get_bool,
        help="중복시 덮어쓸지, 넘어갈지(yes|no, true|false, t|f, y|n, 1|0)",
    )
    args = parser.parse_args()

    try:
        exist_ok = args.force
        target_path = args.target_path

        base_dir = "./test"
        dst_path = os.path.join(base_dir, os.path.basename(target_path))

        print(exist_ok)
        if os.path.exists(dst_path) and exist_ok:
            shutil.rmtree(dst_path)
        elif not exist_ok:
            return

        shutil.copytree(
            src=target_path,
            dst=dst_path,
            dirs_exist_ok=exist_ok,
            copy_function=os.link,
        )

        print({"body": dst_path})
    except Exception as e:
        logging.exception(e, exc_info=True)
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
