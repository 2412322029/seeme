import os

import toml

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, 'data.json')
cfg_path = os.path.join(script_dir, "config.toml")
if not os.path.exists(cfg_path):
    raise FileNotFoundError("config.toml not found")
cfg = toml.load(cfg_path)
SECRET_KEY = cfg.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found")
if not cfg.get("redis"):
    raise ValueError("redis config not found")
# print(cfg)