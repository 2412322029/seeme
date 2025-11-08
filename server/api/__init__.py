import importlib
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
        names = _DEFAULT_SUBMODULES
    for name in names:
        importlib.import_module(f"{pkg}.{name}")


__all__ = ["api_bp", "register_submodules"]
