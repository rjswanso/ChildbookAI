from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

f_app = Flask(__name__)
f_app.config['SECRET_KEY'] = os.environ.get('DB_SECRET_KEY')
f_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Using SQLite as an example

db = SQLAlchemy(f_app)

from routes import *

if __name__ == '__main__':
    f_app.run(debug=True)