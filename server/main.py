from api import api_bp, register_submodules
from flask import Flask

app = Flask(__name__)

register_submodules()
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
