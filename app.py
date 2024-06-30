from flask import Flask
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
