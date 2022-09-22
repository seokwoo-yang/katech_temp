import requests
import json


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

    return response


def post_create_user(base_url, token, username, scope, password):
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

    return response


def download_one(base_url, token, file, type, is_dir):
    url = f"{base_url}/raw/{file}?{f'algo={type}&' if is_dir else ''}auth={token}"
    response = requests.get(url)

    return response


def download_multiple(base_url, token, files, type="zip"):
    url = f"{base_url}/raw/?files={files}&algo={type}&auth={token}"
    response = requests.get(url)

    return response
