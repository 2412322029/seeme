import os
from pprint import pprint

import redis
import json
from config import cfg

r = redis.StrictRedis(**cfg.get("redis"))

Data_limit_default = cfg.get("Data_limit_default")
assert isinstance(Data_limit_default, dict), "Data_limit_default must be a dictionary"
for k, v in Data_limit_default.items():
    if not r.hget("Data_limit", k):
        r.hset("Data_limit", k, v)


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
    return r.get(t)


def limit_hashmap_size(t):
    """
    限制哈希表的大小，删除最旧的键值对
    :param t: type 类型
    :return:
    """
    keys = r.hkeys(t)
    max_size = get_limit(t)
    if keys and len(keys) > max_size:
        sorted_keys = sorted([kk.decode('utf-8') for kk in keys])
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
        return json.loads(r.hget(t, i) or '{}')
    else:
        items = r.hgetall(t)
        items = {ik.decode('utf-8'): json.loads(iv.decode('utf-8')) for ik, iv in items.items()}
        sorted_items = sorted(items.items(), key=lambda x: x[0])
        sorted_values = [value for key, value in sorted_items]
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
        return {ik.decode('utf-8'): int(iv.decode('utf-8')) for ik, iv in r.hgetall("Data_limit").items()}


for t in get_all_types():
    limit_hashmap_size(t)


def load_data():
    data_file = "data.json"
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for dk, dv in data.items():
                for i in dv:
                    r.hset(dk, i["report_time"], json.dumps(i))
    else:
        raise FileNotFoundError(f"{data_file} not found")


# def save_data(d):
#     with open(data_file, 'w') as f:
#         json.dump(d, f, indent=4)


if __name__ == "__main__":
    load_data()
    # pprint(get_all_types_data())
