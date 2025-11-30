import traceback

from flask import Flask

from api import api_bp, register_submodules
from util.logger import logger

try:
    app = Flask(__name__)
    register_submodules()
    app.register_blueprint(api_bp)

    @app.after_request
    def add_cors_headers(response):
        # response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, API-KEY"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response
except Exception as e:
    logger.error(f"{traceback.format_exc()}, Error registering submodules: {e}")
    raise e


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
