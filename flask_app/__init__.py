from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DB = 'flex_schema'
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
KEY = '888e1c1817c4948d34d37f0ffd3e29ea'