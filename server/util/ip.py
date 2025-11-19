import ipaddress

import requests


def is_public_ip(ip: str) -> bool:
    """合法且公网可路由的 IPv4/IPv6"""
    try:
        obj = ipaddress.ip_address(ip)
        return not (obj.is_private | obj.is_loopback | obj.is_link_local | obj.is_multicast | obj.is_reserved)
    except ValueError:
        return False


def ip_api(domain: str) -> str:
    if not is_public_ip(domain):
        return domain
    try:
        url = "http://ip-api.com/json/" + domain
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142 Safari/537.36",
            "Connection": "keep-alive",
            "Referer": "http://www.baidu.com/",
        }
        resp = requests.get(url, headers=headers, timeout=5).json()
        if resp.get("status") == "success":
            return resp["regionName"] + " " + resp["city"]
        return domain
    except Exception:
        return domain


if __name__ == "__main__":
    print(ip_api("223.77.170.173"))
