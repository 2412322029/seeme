import logging
import os
from logging.handlers import RotatingFileHandler

from flask import has_request_context, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if os.path.exists("log") is False:
    os.mkdir("log")


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
            record.remote_addr = request.headers.get("CF-Connecting-IP", ip)
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


file_handler = RotatingFileHandler(
    filename="log/app.log",
    maxBytes=1024 * 1024 * 5,
    backupCount=5,
)
file_handler.setFormatter(RequestFormatter("%(asctime)s %(levelname)s %(remote_addr)s - %(url)s : %(message)s [in %(filename)s:%(lineno)d]"))
logger.addHandler(file_handler)
