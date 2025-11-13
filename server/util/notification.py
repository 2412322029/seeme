import json

import requests

from util.config import cfg


def notify(title, content, type):
    if not cfg.get("notification", {}).get("enable", False):
        return
    methods = cfg.get("notification", {}).get("methods", [])
    if "pushplus" in methods:
        pushplus_notify(title, content, type)
    else:
        print("No notification method configured.")


def pushplus_notify(title, content, type="markdown"):
    token = cfg.get("notification", {}).get("pushplus", {}).get("token", "")
    if not token:
        return
    url = "http://www.pushplus.plus/send"
    data = {"token": token, "title": title, "content": content, "template": type}
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, data=body, headers=headers).json()
    if resp.get("code") != 200:
        print("Pushplus notification failed:", resp)
    else:
        print(f"Pushplus notification sent successfully. {resp}")

if __name__ == "__main__":
    notify("测试通知", "这是一条测试通知内容。", "markdown")