import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))


class MyCache:
    def __init__(self, storage_file=os.path.join(script_dir, "cache.json")):
        self.storage_file = storage_file
        self._initialize_storage()

    def _initialize_storage(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as f:
                json.dump({}, f)

    def _load_data(self):
        with open(self.storage_file, "r") as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def set(self, name: str, value):
        data = self._load_data()
        data[name] = value
        self._save_data(data)

    def get(self, name: str):
        data = self._load_data()
        return data.get(name)

    def hset(self, name: str, key: str, value):
        data = self._load_data()
        if name not in data:
            data[name] = {}
        data[name][key] = value
        self._save_data(data)

    def hget(self, name: str, key: str):
        data = self._load_data()
        return data.get(name, {}).get(key)

    def hdel(self, name: str, *keys: str):
        data = self._load_data()
        if name in data:
            for key in keys:
                if key in data[name]:
                    del data[name][key]
            if not data[name]:
                del data[name]
        self._save_data(data)

    def hkeys(self, name: str):
        data = self._load_data()
        return list(data.get(name, {}).keys())

    def hgetall(self, name: str):
        data = self._load_data()
        return data.get(name, {})
