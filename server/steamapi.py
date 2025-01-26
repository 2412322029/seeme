import requests

from config import cfg


def steam_info():
    if not cfg.get("steam")["enable"]:
        return {"steam_enable": False}
    steam_id = cfg.get("steam")["steam_id"]
    steam_key = cfg.get("steam")["steam_key"]
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
                        f"?key={steam_key}&steamids={steam_id}")
    if resp.status_code == 200:
        return {"steam_enable": True, "status_code": resp.status_code, "data": resp.json()}
    else:
        return {"steam_enable": True, "status_code": resp.status_code, "text": resp.text}


if __name__ == '__main__':
    print(steam_info())
