from dataclasses import dataclass
import requests

import logging.config
import logging
import pathlib
import argparse
import json

import config


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

    base_url = "http://192.168.101.44:8080/api"
    token = get_token(base_url)
    status = post_create_user(base_url, username, scope, password, token)

    return status


def get_token(base_url):
    """
    파일브라우저의 로그인 API를 호출하여 인증 토큰을 발급받고 리턴

    Args:
        base_url (str): 파일브라우저 base url
    Returns:
        str: 인증토큰
    """
    url = base_url + "/login"
    headers = {"X-pass-user": "admin"}
    response = requests.post(url, headers=headers)

    return response.text


def post_create_user(base_url, username, scope, password, token):
    """
    파일브라우저의 계정 생성 API를 호출하고 성공 여부를 리턴

    Args:
        base_url (str): 파일브라우저 base url
        username (str): 생성할 계정명
        scope (str): 홈디렉토리
        password (str): 패스워드
        token (str): 로그인을 통해 발급받은 인증토큰

    Returns:
        int: 상태코드
    """
    url = base_url + "/users"
    data = {
        "what": "user",
        "which": [],
        "data": {
            "scope": scope,
            "locale": "en",
            "viewMode": "mosaic",
            "singleClick": False,
            "sorting": {"by": "", "asc": False},
            "perm": {
                "admin": False,
                "execute": True,
                "create": True,
                "rename": True,
                "modify": True,
                "delete": True,
                "share": True,
                "download": True,
            },
            "commands": [],
            "hideDotfiles": False,
            "dateFormat": False,
            "username": username,
            "passsword": "",
            "rules": [],
            "lockPassword": False,
            "id": 0,
            "password": password,
        },
    }

    headers = {"X-Auth": token}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.headers)

    return response.status_code


def main():
    logging.config.dictConfig(config.logging_config(f"{pathlib.Path(__file__).stem}.log"))

    parser = argparse.ArgumentParser(description="파일 미리보기")
    parser.add_argument("--username", required=True, help="생성할 사용자명")
    parser.add_argument("--scope", required=True, help="사용자 홈 디렉토리 경로")
    parser.add_argument("--password", required=True, help="사용자 패스워드")
    args = parser.parse_args()

    try:
        username = args.username
        scope = args.scope
        password = args.password
        rows = {"body": create_user(username, scope, password)}

        print(rows)
    except Exception as e:
        logging.exception(e, exc_info=True)
        print({"body": [], "message": f"fail :: {str(e)}"})


if __name__ == "__main__":
    main()
