import ipaddress
from pathlib import Path
import geoip2.database

DB_FILE = Path(__file__).with_name('GeoLite2-City.mmdb')
if not DB_FILE.is_file():
    raise SystemExit(f'{DB_FILE} not found, please download it from https://github.com/P3TERX/GeoLite.mmdb')
reader = geoip2.database.Reader(DB_FILE)
def is_public_ip(ip: str) -> bool:
    """合法且公网可路由的 IPv4/IPv6"""
    try:
        obj = ipaddress.ip_address(ip)
        return not (
            obj.is_private |
            obj.is_loopback |
            obj.is_link_local |
            obj.is_multicast |
            obj.is_reserved
        )
    except ValueError:
        return False

def locateip(ip):
    try:
        if not is_public_ip(ip):
            return None
        r = reader.city(ip)
        return {
                'country': r.country.name,
                'country_iso': r.country.iso_code,
                'subdiv': r.subdivisions.most_specific.name,   # 省/州
                'city': r.city.name,
                'lat': r.location.latitude,
                'lon': r.location.longitude,
                'tz': r.location.time_zone,
                'postal': r.postal.code,
            }
    except geoip2.errors.AddressNotFoundError:
        return None

if __name__ == '__main__':
    print(locateip('223.77.170.173'))
