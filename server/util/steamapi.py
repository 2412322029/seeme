import functools

import requests

from .config import cfg


def steam_info():
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_id = cfg.get("steam", {}).get("steam_id", "")
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_key}&steamids={steam_id}")
    if resp.status_code == 200:
        return {
            "steam_enable": True,
            "status_code": resp.status_code,
            "data": resp.json(),
        }
    else:
        return {
            "steam_enable": True,
            "status_code": resp.status_code,
            "text": resp.text,
        }


@functools.lru_cache(maxsize=1)
def steam_friend_list(ret_ids=False, t=None):
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_id = cfg.get("steam", {}).get("steam_id", "")
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    try:
        resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={steam_key}&steamid={steam_id}#{t}")
        if not ret_ids:
            if resp.status_code == 200:
                return {
                    "steam_enable": True,
                    "status_code": resp.status_code,
                    "data": resp.json(),
                }
            else:
                return {
                    "steam_enable": True,
                    "status_code": resp.status_code,
                    "text": resp.text,
                }
        else:
            if resp.status_code == 200:
                return ",".join([i["steamid"] for i in resp.json()["friendslist"]["friends"]])
            else:
                return None
    except Exception:
        return None


steam_ids = steam_friend_list(ret_ids=True)


def sort_players(players):
    """
    Sort players so that online players come first, then by lastlogoff (most recent first).
    Online is defined as personastate > 0.
    """
    if not isinstance(players, list):
        return players
    return sorted(
        players,
        key=lambda p: (
            0 if p.get("personastate", 0) > 0 else 1,
            -int(p.get("lastlogoff", 0)),
        ),
    )


def steam_friend_info():
    if not cfg.get("steam", {}).get("enable", ""):
        return {"steam_enable": False}
    steam_key = cfg.get("steam", {}).get("steam_key", "")
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_key}&steamids={steam_ids}")

    if resp.status_code == 200:
        data = resp.json()
        # If the response contains a players list, sort it (online first, then lastlogoff desc)
        try:
            players = data.get("response", {}).get("players")
            if players:
                data["response"]["players"] = sort_players(players)
        except Exception:
            # If any unexpected structure, just ignore sorting and return raw data
            pass
        return {"steam_enable": True, "status_code": resp.status_code, "data": data}
    else:
        return {
            "steam_enable": True,
            "status_code": resp.status_code,
            "text": resp.text,
        }


if __name__ == "__main__":
    print(steam_friend_info())
