import multiprocessing

# 工作进程数，通常设置为 (CPU核心数 * 2) + 1
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2  # 每个工作进程的线程数
bind = "127.0.0.1:5000"
# SSL证书路径
# certfile = "/var/www/seeme/ssl/i.not404.cc.pem"
# keyfile = "/var/www/seeme/ssl/i.not404.cc.key"

pidfile = "/var/www/seeme/gunicorn.pid"
loglevel = "info"  # 日志级别
timeout = 30  # 超时时间

# gunicorn -c gunicorn.conf.py main:app -D

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["error_file"]},
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_file"],  # 错误日志使用文件处理器
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_file"],  # 访问日志使用文件处理器
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
    "handlers": {
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",  # 按时间分割
            "filename": "/var/www/seeme/log/gunicorn_error.log",
            "when": "D",  # 按天分割（D=天，H=小时，M=分钟）
            "interval": 1,
            "backupCount": 30,  # 保留30个备份文件
            "formatter": "generic",
            "encoding": "UTF-8",
        },
        "access_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/var/www/seeme/log/gunicorn_access.log",
            "when": "D",
            "interval": 1,
            "backupCount": 30,
            "formatter": "generic",
            "encoding": "UTF-8",
        },
    },
}
