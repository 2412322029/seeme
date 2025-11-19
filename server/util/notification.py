import requests
from util.config import cfg
from util.logger import logger


def notify(title, content):
    if not cfg.get("notification", {}).get("enabled", False):
        return
    methods = cfg.get("notification", {}).get("methods", [])
    if "pushplus" in methods:
        pushplus_notify(title, content)
    else:
        logger.error("No notification method configured.")


def pushplus_notify(title, content: str):
    token = cfg.get("notification", {}).get("pushplus", {}).get("token", "")
    if not token:
        return
    url = "http://www.pushplus.plus/send"
    data = {
        "token": token,
        "title": title,
        "content": content.replace("\n", "<br>"),
        "template": "markdown",
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=data, headers=headers).json()
    if resp.get("code") != 200:
        logger.error("Pushplus notification failed:", resp)
    else:
        logger.info(f"Pushplus notification sent successfully. {resp}")
