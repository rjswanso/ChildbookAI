from flask import Flask
from flask_sqlalchemy import SQLAlchemy

f_app = Flask(__name__)
f_app.config['SECRET_KEY'] = 'secret-key'
f_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Using SQLite as an example

db = SQLAlchemy(f_app)

from routes import *

if __name__ == '__main__':
    f_app.run(debug=True)