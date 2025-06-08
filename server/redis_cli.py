import redis
import json
import argparse
import os


# 连接到Redis服务器
def connect_redis(host='127.0.0.1', port=6379, db=0, password=None):
    return redis.Redis(host=host, port=port, db=db, password=password)


# 获取键的类型
def get_key_type(redis_client, key):
    return redis_client.type(key).decode('utf-8')


# 获取键的值，根据键的类型
def get_key_value(redis_client, key):
    key_type = get_key_type(redis_client, key)
    if key_type == 'string':
        return redis_client.get(key).decode('utf-8')
    elif key_type == 'list':
        return [item.decode('utf-8') for item in redis_client.lrange(key, 0, -1)]
    elif key_type == 'set':
        return {item.decode('utf-8') for item in redis_client.smembers(key)}
    elif key_type == 'zset':
        return [(item[0].decode('utf-8'), item[1]) for item in redis_client.zrange(key, 0, -1, withscores=True)]
    elif key_type == 'hash':
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in redis_client.hgetall(key).items()}
    else:
        return None


# 导出指定键的数据到JSON文件
def export_keys(redis_client, keys, filename):
    data = {}
    for key in keys:
        value = get_key_value(redis_client, key)
        if value is not None:
            data[key] = value
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, default=str)
    print(f"Data exported to {filename}")


# 导入JSON文件中的数据到Redis
def import_keys(redis_client, filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return
    with open(filename, 'r') as f:
        data = json.load(f)
    for key, value in data.items():
        key_type = get_key_type(redis_client, key)
        if key_type == 'string':
            redis_client.set(key, value)
        elif key_type == 'list':
            redis_client.rpush(key, *value)
        elif key_type == 'set':
            redis_client.sadd(key, *value)
        elif key_type == 'zset':
            for item in value:
                redis_client.zadd(key, {item[0]: item[1]})
        elif key_type == 'hash':
            redis_client.hmset(key, value)
    print(f"Data imported from {filename}")


# 主函数
def main():
    parser = argparse.ArgumentParser(description="Redis Import/Export CLI")
    parser.add_argument('--host', default='127.0.0.1', help='Redis host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=6379, help='Redis port (default: 6379)')
    parser.add_argument('--db', type=int, default=0, help='Redis database (default: 0)')
    parser.add_argument('--password', help='Redis password (default: None)')
    parser.add_argument('--export', nargs='+', help='Export specified keys to a JSON file')
    parser.add_argument('--import-file', help='Import data from a JSON file')
    parser.add_argument('--output', help='Output file for export (default: export.json)')
    args = parser.parse_args()

    redis_client = connect_redis(args.host, args.port, args.db, args.password)

    if args.export:
        keys = args.export
        output_file = args.output if args.output else 'export.json'
        export_keys(redis_client, keys, output_file)
    elif args.import_file:
        import_keys(redis_client, args.import_file)
    else:
        print("Please specify --export or --import-file option.")


if __name__ == '__main__':
    main()
