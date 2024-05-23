from datetime import datetime
import json, requests, base64


def check_username(username: str) -> str | None:
    timestamp = datetime.now().timestamp()
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}?at={timestamp}"

    response = requests.get(url=url)
    if not response.status_code == 200:
        return None
    else:
        return json.loads(response.text).get('name')
    