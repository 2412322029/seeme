import winreg


def requery(k, n):
    try:
        return winreg.QueryValueEx(k, n)[0]
    except Exception:
        return ""


def get_software_version_from_registry(path=None, name=None):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    try:
                        display_name = requery(subkey, "DisplayName")
                        install_location = requery(subkey, "InstallLocation")
                        if not install_location:
                            install_location = requery(subkey, "InstallPath")
                        display_version = requery(subkey, "DisplayVersion")
                        url_info_about = requery(subkey, "URLInfoAbout")
                        if not url_info_about:
                            url_info_about = requery(subkey, "HelpLink")
                        publisher = requery(subkey, "Publisher")
                        a = {
                            "display_name": display_name,
                            "install_location": install_location,
                            "url_info_about": url_info_about,
                            "display_version": display_version,
                            "publisher": publisher
                        }
                        if path:
                            if path in install_location:
                                return a
                        if name:
                            if name in display_name:
                                return a
                    except FileNotFoundError:
                        pass
    except FileNotFoundError:
        pass

# pprint(get_software_version_from_registry(path=r"D:\soft\PyCharm Community Edition 2023.3.2\bin"))
