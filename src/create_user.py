import logging
import requests
import argparse
import json
from common.filebrowser import get_token, post_create_user

from common.config import get_config


CONFIG = get_config()


def create_user(username, scope, password):
    """
    파일브라우저의 사용자 생성 API 호출


    Args:
        username (str): 사용자명
        scope (str): 사용자 홈 디렉토리
        password (str): 사용자 패스워드
    Returns:
        int: 응답 상태코드
    """

    base_url = f"{CONFIG.FILEBROWSER.CONN_URL}/api"
    token = get_token(base_url).text
    status = post_create_user(base_url, token, username, scope, password).status_code

    return status


def main():
    parser = argparse.ArgumentParser(description="파일브라우저 계정 생성")
    parser.add_argument("--username", required=True, help="생성할 사용자명")
    parser.add_argument("--password", required=True, help="사용자 패스워드")
    parser.add_argument("--scope", required=False, default=None, help="사용자 홈 디렉토리 경로(default: /계정명)")
    args = parser.parse_args()

    try:
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)

        username = args.username
        password = args.password
        scope = "/" + username if args.scope in (".", "/", None) else args.scope
        rows = {"body": create_user(username, scope, password)}

        print(rows)
    except Exception as e:
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
