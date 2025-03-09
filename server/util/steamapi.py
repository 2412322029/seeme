import functools

import requests

from .config import cfg


def steam_info():
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_id = cfg.get("steam", {}).get("steam_id", "")
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
                        f"?key={steam_key}&steamids={steam_id}")
    if resp.status_code == 200:
        return {"steam_enable": True, "status_code": resp.status_code, "data": resp.json()}
    else:
        return {"steam_enable": True, "status_code": resp.status_code, "text": resp.text}


@functools.lru_cache(maxsize=1)
def steam_friend_list(ret_ids=False, t=None):
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_id = cfg.get("steam", {}).get("steam_id", "")
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    try:
        resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
                            f"?key={steam_key}&steamid={steam_id}#{t}")
        if not ret_ids:
            if resp.status_code == 200:
                return {"steam_enable": True, "status_code": resp.status_code, "data": resp.json()}
            else:
                return {"steam_enable": True, "status_code": resp.status_code, "text": resp.text}
        else:
            if resp.status_code == 200:
                return ','.join([i['steamid'] for i in resp.json()['friendslist']['friends']])
            else:
                return None
    except Exception:
        return None


steam_ids = steam_friend_list(ret_ids=True)


def steam_friend_info():
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
                        f"?key={steam_key}&steamids={steam_ids}")
    if resp.status_code == 200:
        return {"steam_enable": True, "status_code": resp.status_code, "data": resp.json()}
    else:
        return {"steam_enable": True, "status_code": resp.status_code, "text": resp.text}


if __name__ == '__main__':
    print(steam_friend_info())
