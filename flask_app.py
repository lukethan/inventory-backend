
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="kegsouth",
    password="kegsouthpinecrest",
    hostname="kegsouth.mysql.pythonanywhere-services.com",
    databasename="kegsouth$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Inventory(db.Model):

    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(30), unique=True, nullable=False)
    image = db.Column(db.String(250))
    amount = db.Column(db.Integer, nullable=False)


products = []



