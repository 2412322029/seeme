import importlib
import pkgutil
from typing import Iterable, Optional

from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

_DEFAULT_SUBMODULES = [
    "paste",
    "pubinfo",
    "info",
    "icons",
    "steam",
    "misc",
    "messages",
]


def register_submodules(names: Optional[Iterable[str]] = None) -> None:
    pkg = __package__ or "api"
    if names is None:
        # 自动发现当前包下的模块（排除以 "_" 开头的私有模块）
        try:
            package = importlib.import_module(pkg)
            discovered = [
                modname
                for _, modname, _ in pkgutil.iter_modules(package.__path__)
                if not modname.startswith("_")
            ]
            names = sorted(discovered)
        except Exception:
            names = _DEFAULT_SUBMODULES

    for name in names:
        importlib.import_module(f"{pkg}.{name}")


__all__ = ["api_bp", "register_submodules"]
