import json
from datetime import datetime

from util.logger import logger

from .config import cfg
from .mycache import MyCache

if cfg.get("without_redis"):
    r = MyCache()
    logger.info("use mycache 不支持多线程!")
else:
    import redis

    # 使用连接池
    pool = redis.ConnectionPool(**cfg.get("redis"))
    r = redis.StrictRedis(connection_pool=pool)
    logger.info("use redis")

Data_limit_default = cfg.get("Data_limit_default")
assert isinstance(Data_limit_default, dict), "Data_limit_default must be a dictionary"
for k, v in Data_limit_default.items():
    if not r.hget("Data_limit", k):
        r.hset("Data_limit", k, v)


def if_decode(s: any):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        # 修复乱码：正确使用 utf-8 解码
        return s.decode("utf-8")
    else:
        return s


def key_to_ts(k: any) -> int:
    """
    把 hashmap 的 key 转成时间戳（秒），以便按时间排序。
    支持的 key 格式：
    - 纯数字字符串（例如 '1737204278'） -> 直接转 int
    - 格式化时间字符串（例如 '2025/1/23 10:27:49' 或 '2025-01-23 10:27:49'）
    如果无法解析，返回 0 作为兜底。
    """
    if isinstance(k, (int, float)):
        return int(k)
    s = str(k)
    s = s.strip()
    # 纯数字为 epoch
    if s.isdigit():
        try:
            return int(s)
        except Exception:
            pass

    # 尝试多种常见的时间格式
    fmts = (
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d",
        "%Y-%m-%d",
    )
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            return int(dt.timestamp())
        except Exception:
            continue

    # 最后尝试按 float 解析
    try:
        return int(float(s))
    except Exception:
        return 0


def get_all_types():
    return list(Data_limit_default.keys())


def put_data(t, dic):
    """

    :param t: type 类型
    :param dic: 字典数据必须包含report_time
    :return:
    """
    r.hset(t, dic["report_time"], json.dumps(dic))
    limit_hashmap_size(t)


def set_data(t, d):
    r.set(t, d)


def get_data(t):
    res = r.get(t)
    if res:
        return if_decode(res)
    else:
        return "{}"


def limit_hashmap_size(t):
    """
    限制哈希表的大小，删除最旧的键值对
    :param t: type 类型
    :return:
    """
    keys = r.hkeys(t)
    max_size = get_limit(t)
    if keys and len(keys) > max_size:
        sorted_keys = sorted([if_decode(kk) for kk in keys])
        for key in sorted_keys[:-max_size]:
            # print(key)
            r.hdel(t, key)


def get_1type_data(t, i=None):
    """
    :param t: type 类型
    :param i: hashmap 的 key 即为 report_time ,缺省返回所有值的排完序列表
    :return:
    """

    if i:
        return json.loads(r.hget(t, i) or "{}")
    else:
        items = r.hgetall(t)
        # decode keys/values
        items = {if_decode(ik): json.loads(if_decode(iv)) for ik, iv in items.items()}
        # 按时间排序（使用 key_to_ts 支持多种 key 格式）
        sorted_items = sorted(items.items(), key=lambda x: key_to_ts(x[0]))
        sorted_values = [value for key, value in sorted_items]  # key是2025/1/23 10:27:49或1737204278格式，按时间排序
        return {t: sorted_values}


def del_data(t, report_time):
    """
    删除特定类型和报告时间的键值对
    :param t: type 类型
    :param report_time: 报告时间
    :return:
    """
    result = r.hdel(t, report_time)
    return result


def get_all_types_data():
    d = {}
    for t in get_all_types():
        d.update(get_1type_data(t))
    return d


def set_limit(t, n):
    r.hset("Data_limit", t, n)
    limit_hashmap_size(t)


def get_limit(t=None):
    """

    :param t: type 类型
    :return:
    """
    if t:
        return int(r.hget("Data_limit", t))
    else:
        return {if_decode(ik): int(if_decode(iv)) for ik, iv in r.hgetall("Data_limit").items()}


for t in get_all_types():
    limit_hashmap_size(t)
