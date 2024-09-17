
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

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

    def __repr__(self):
        return f'<Inventory(id={self.id}, item={self.item}, amount={self.amount})>'


    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'image': self.image,
            'amount': self.amount
        }

"""
Example for how to add a row to database
products = Inventory(item="Coors", image="", amount="10")
db.session.add(products)
db.session.commit()
"""

inventory = {
    1: {'item': 'coors', 'amount': 10}
}


# product1 = Inventory(item="Coors", image="", amount="8")

# try:
#     db.session.add(product1)
#     db.session.commit()
# except:
#     pass


class Inventory_API(Resource):
    def get(self):
        products = Inventory.query.all()
        return jsonify([product.to_dict() for product in products])
    def post(self):
        # Initialize a parser to handle incoming data
        parser = reqparse.RequestParser()
        parser.add_argument('item', type=str, required=True, help='Item name is required')
        parser.add_argument('amount', type=int, required=True, help='Amount is required')
        args = parser.parse_args()

        item_id = len(inventory) + 1  # Generate a new ID (simple approach, can be improved)
        item_name = args['item']
        amount = args['amount']

        # Add the new item to the inventory
        inventory[item_id] = {
            'item': item_name,
            'amount': amount
        }

        return jsonify({
            'message': f"New inventory item added with ID: {item_id}",
            'item': {
                'id': item_id,
                'item': item_name,
                'amount': amount
            }
        })


api.add_resource(Inventory_API, '/')

if __name__ == '__main__':
    app.run(debug=True)




