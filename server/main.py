from flask import Flask

from api import api_bp, register_submodules

app = Flask(__name__)

register_submodules()
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
