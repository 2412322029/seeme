import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

script_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本文件目录
log_dir = os.path.join(script_dir, 'log')  # 日志目录
os.makedirs(log_dir, exist_ok=True)  # 创建日志目录
log_file = f"{log_dir}/report.{datetime.now().strftime('%Y-%m-%d')}.log"  # 日志文件


def setup_logger(logger_name="main", log_level=logging.INFO):
    fm = "%(asctime)-15s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s"
    logging.basicConfig(format=fm, level=log_level)
    l = logging.getLogger(logger_name)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=30, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(fm))
    l.addHandler(file_handler)
    return l


logger = setup_logger(script_dir)
