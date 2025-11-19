import asyncio
import contextlib
import logging
import os
import socket
from typing import Optional

from mcstatus import BedrockServer, JavaServer
from mcstatus.responses import BedrockStatusResponse, JavaStatusPlayer, JavaStatusResponse


class Protocol:
    AUTO = "auto"
    JAVA = "java"
    BEDROCK = "bedrock"


def JavaStatusPlayer2list(j: list[JavaStatusPlayer] | None):
    players: list[dict[str, str]] = []
    if not j:
        return players
    for i in j:
        players.append({"name": i.name, "uuid": i.id})
    return players


def JavaStatusResponse2json(s: JavaStatusResponse, latency: float):
    json_str = {
        "type": "java",
        "enforces_secure_chat": s.enforces_secure_chat,
        "version": {"name": s.version.name, "protocol": s.version.protocol},
        "players": {
            "online": s.players.online,
            "max": s.players.max,
            "sample": JavaStatusPlayer2list(s.players.sample),
        },
        "motd": {"plain": s.motd.to_plain(), "html": s.motd.to_html()},
        "latency": format(latency, ".2f") + " ms",
        "icon": s.icon,
        "forge_data": {
            "fml_network_version": s.forge_data.fml_network_version,
            "channels": [
                {
                    "name": c.name,
                    "version": c.version,
                    "required": c.required,
                }
                for c in s.forge_data.channels
            ],  # Mod间通信所使用的频道列表，可能包括注册名、版本以及通信协议等属性。
            "mods": [
                {
                    "modid": m.name,
                    "version": m.marker,
                }
                for m in s.forge_data.mods
            ],
            "truncated": s.forge_data.truncated,  # 一个标志位，指示mods列表或channels列表是否不完整（被截断）
        }
        if s.forge_data
        else None,
    }
    return json_str


def BedrockStatusResponse2json(s: BedrockStatusResponse):
    json_str = {
        "type": "bedrock",
        "version": {"name": s.version.name, "protocol": s.version.protocol},
        "map_name": s.map_name,
        "gamemode": s.gamemode,
        "players": {
            "online": s.players.online,
            "max": s.players.max,
        },
        "motd": {"plain": s.motd.to_plain(), "html": s.motd.to_html()},
        "latency": format(s.latency, ".2f") + " ms",
    }
    return json_str


async def try_java(a):
    try:
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stderr(devnull):
                server = await JavaServer.async_lookup(a)
                status_task = server.async_status()
                ping_task = server.async_ping()
                status_res, ping_res = await asyncio.gather(status_task, ping_task, return_exceptions=True)
        if isinstance(status_res, Exception):
            raise status_res
        latency = -1.0 if isinstance(ping_res, Exception) else ping_res
        return JavaStatusResponse2json(status_res, latency)
    except (BrokenPipeError, ConnectionResetError, socket.error, OSError) as e:
        msg = f"network error {e}"
        logging.getLogger(__name__).warning(msg)
        return {"_error": msg}
    except Exception as e:
        return {"_error": str(e)}


async def try_bedrock(a):
    try:
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stderr(devnull):
                server = BedrockServer.lookup(a)
                status = await server.async_status()
        return BedrockStatusResponse2json(status)
    except (BrokenPipeError, ConnectionResetError, socket.error, OSError) as e:
        msg = f"network error, {e}"
        logging.getLogger(__name__).warning(msg)
        return {"_error": msg}
    except Exception as e:
        return {"_error": str(e)}


def mcinfo(address: str, protocol: Optional[Protocol] = None) -> dict:
    """
    获取服务器信息。
    protocol: Protocol.JAVA / Protocol.BEDROCK / Protocol.AUTO(None)。
    若为 AUTO(或 None), 同时尝试 Java Bedrock，优先返回成功结果。
    """
    proto = protocol or Protocol.AUTO
    addr = address
    if address.startswith("bedrock://"):
        addr = address[len("bedrock://") :]
        proto = Protocol.BEDROCK
    elif address.startswith("java://"):
        addr = address[len("java://") :]
        proto = Protocol.JAVA
    if proto == Protocol.JAVA:
        res = asyncio.run(try_java(addr))
        return res if "error" in res or "_error" not in res else {"error": res.get("_error")}
    if proto == Protocol.BEDROCK:
        res = asyncio.run(try_bedrock(addr))
        return res if "error" in res or "_error" not in res else {"error": res.get("_error")}
    if proto == Protocol.AUTO:

        async def _gather_both(a):
            return await asyncio.gather(try_java(a), try_bedrock(a), return_exceptions=True)

        res_java, res_bedrock = asyncio.run(_gather_both(addr))

        def _to_dict(r):
            if isinstance(r, Exception):
                return {"_error": str(r)}
            return r

        java_res = _to_dict(res_java)
        bedrock_res = _to_dict(res_bedrock)
        if "error" not in java_res and "_error" not in java_res:
            return java_res
        if "error" not in bedrock_res and "_error" not in bedrock_res:
            return bedrock_res

        err = java_res.get("_error") or bedrock_res.get("_error") or "unknown error"
        return {"error": err}


if __name__ == "__main__":
    from pprint import pprint

    # pprint(mcinfo("k3.mchx.ltd:10011", "java"))
    # pprint(mcinfo(address="demo.mcstatus.io", protocol="java"))
    # pprint(mcinfo(address="play.edgerunners.cn:30737", protocol="java"))
    pprint(mcinfo(address="play.edgerunners.cn:30714", protocol="java"))
    # pprint(mcinfo("mc.hypixel.net"))
