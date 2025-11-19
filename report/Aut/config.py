import configparser
import os

from .logger import APPDATA

CONFIG_FILE = os.path.join(APPDATA, "config.ini")


def setting_config(config_dict):
    """
    :param config_dict: 一个 字典，包含配置项["DEFAULT"]
    """
    try:
        cfg = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            cfg.read(CONFIG_FILE)
        else:
            cfg.add_section("DEFAULT")
        for key, value in config_dict["DEFAULT"].items():
            cfg.set("DEFAULT", key, value)
        with open(CONFIG_FILE, "w") as configfile:
            cfg.write(configfile)
        return True, f"Config file created/updated at: {CONFIG_FILE}"
    except Exception as e:
        return False, str(e)


def read_config():
    """
    从配置文件中读取配置。
    :return: 一个 字典，包含所有配置项
    """
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config
    else:  # 初始化
        config.set("DEFAULT", "key", "")
        config.set("DEFAULT", "url", "")
        config.set(
            "DEFAULT",
            "exclude_process",
            "TextInputHost.exe,SystemSettings.exe,NVIDIA Overlay.exe,svchost.exe,ApplicationFrameHost.exe",
        )
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
        return config


cfg = read_config()
