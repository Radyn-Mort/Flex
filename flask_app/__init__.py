from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DB = 'flex_schema'
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)