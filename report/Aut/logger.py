import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

__version__ = "0.1.7"
__buildAt__ = "2025-03-01 14:03:12"
APPDATA = os.path.dirname(os.path.abspath(__file__))  # 脚本文件目录
if sys.platform == "win32":
    APPDATA = os.path.join(os.environ["LOCALAPPDATA"], "seeme-report")
else:
    raise EnvironmentError("This script is designed for Windows.")
os.makedirs(APPDATA, exist_ok=True)
log_dir = os.path.join(APPDATA, 'log')  # 日志目录
os.makedirs(log_dir, exist_ok=True)  # 创建日志目录
log_file = f"{log_dir}/report.{datetime.now().strftime('%Y-%m-%d')}.log"  # 日志文件


def setup_logger(logger_name="main", log_level=logging.INFO):
    # [%(threadName)s]
    fm = "%(asctime)-12s [%(levelname)s] [%(filename)s %(funcName)s:%(lineno)d] %(message)s"
    logging.basicConfig(format=fm, level=log_level, handlers=[logging.StreamHandler(sys.stdout)])
    lo = logging.getLogger(logger_name)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=30, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(fm))
    lo.addHandler(file_handler)
    return lo


logger = setup_logger()
# print(f"{APPDATA=}")
