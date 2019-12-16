from flask import Flask
from frontend.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from frontend import route
