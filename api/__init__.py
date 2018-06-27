import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
dbase = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/dtr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'
app.debug = True

from models import *
dbase.create_all()
