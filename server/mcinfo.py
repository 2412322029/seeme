import json

from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse, JavaStatusPlayer


def JavaStatusPlayer2list(j: list[JavaStatusPlayer] | None):
    l: list[dict[str, str]] = []
    if not j:
        return l
    for i in j:
        l.append({"name": i.name, "uuid": i.id})
    return l


def JavaStatusResponse2json(s: JavaStatusResponse):
    json_str = json.dumps({
        "version": {
            "name": s.version.name,
            "protocol": s.version.protocol
        },
        "players": {
            "online": s.players.online,
            "max": s.players.max,
            "sample": JavaStatusPlayer2list(s.players.sample)
        },
        "motd": {
            "plain": s.motd.to_plain(),
            "html": s.motd.to_html()
        },
        "icon": s.icon
    }, indent=4)
    return json_str


def mcinfo(address: str) -> str | dict:
    try:
        server = JavaServer.lookup(address)
        status = server.status()
        return JavaStatusResponse2json(status)
    except Exception as e:
        return str(e)


def mclatency(address: str):
    try:
        server = JavaServer.lookup(address)
        latency = server.ping()
        return f"{int(latency)} ms"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    print(mclatency("demo.mcstatus.io:25565"))
    print(mcinfo("demo.mcstatus.io:25565"))
