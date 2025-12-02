from os import getenv

from dotenv import load_dotenv
from flask import Flask

from .api import mount_routes
from .error import set_error_handler
from .service.swagger import setup_swagger

load_dotenv()

app = Flask(__name__)

with app.app_context():
    setup_swagger()
    mount_routes()
    set_error_handler()

if __name__ == "__main__":
    app.run("0.0.0.0", getenv("PORT", 5000))
