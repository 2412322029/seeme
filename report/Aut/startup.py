import winreg

STARTUP_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def set_startup(name, path):
    """设置开机启动项"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY_PATH, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
        print(f"开机启动项 '{name}' 已设置成功！")
    except Exception as e:
        print(f"设置失败：{e}")


def check_startup_exists(name):
    """检查开机启动项是否存在"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, name)
            return 1
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"检查启动项时发生错误：{e}")
        return 0


def get_startup(name):
    """获取开机启动项的值"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY_PATH, 0, winreg.KEY_READ) as key:
            value, value_type = winreg.QueryValueEx(key, name)
            if value_type == winreg.REG_SZ:
                print(f"启动项 '{name}' 的值为：{value}")
                return str(value)
            else:
                print(f"启动项 '{name}' 的值类型不正确！")
    except FileNotFoundError:
        print(f"启动项 '{name}' 不存在！")
    except Exception as e:
        print(f"获取失败启动项：{e}")


def delete_startup(name):
    """删除开机启动项"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY_PATH, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, name)
        print(f"开机启动项 '{name}' 已删除成功！")
    except FileNotFoundError:
        print(f"启动项 '{name}' 不存在，无需删除！")
    except Exception as e:
        print(f"删除失败：{e}")


if __name__ == "__main__":
    # set_startup('seeme-report', r'D:\24123\code\py\wayd\report\dist\report_gui.dist\report.exe aut')
    get_startup('seeme-report')
