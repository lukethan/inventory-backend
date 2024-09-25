
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


app = Flask(__name__)
api = Api(app)
CORS(app)
# load_dotenv()

project_folder = os.path.expanduser('~/mysite')
load_dotenv(os.path.join(project_folder, '.env'))

"""
CORS Instructions:
CORS(app, origins=["https://your-frontend-domain.com"])
CORS(app, methods=["GET", "POST"], allow_headers=["Content-Type"])
@app.route('/your-endpoint')
@cross_origin()  # Apply CORS to this specific route
def your_endpoint():
    return {'message': 'Hello, world!'}
"""
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
hostname = os.getenv('HOSTNAME')
databasename = os.getenv('DATABASENAME')

SQLALCHEMY_DATABASE_URI = (f"mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}")

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

inventory = {1: {'item': 'coors', 'amount': 10}}
product1 = Inventory(item="Coors", image="", amount="8")
try:
    db.session.add(product1)
    db.session.commit()
except:
    pass
"""

class Inventory_API(Resource):
    def get(self):
        products = Inventory.query.order_by(Inventory.amount).all()
        return jsonify([product.to_dict() for product in products])
    def post(self):
        # Initialize a parser to handle incoming data
        parser = reqparse.RequestParser()
        parser.add_argument('item', type=str, required=True, help='Item name is required')
        parser.add_argument('amount', type=int, required=True, help='Amount is required')
        parser.add_argument('image', type=str, required=False, default="")
        args = parser.parse_args()

        item = args['item']
        amount = args['amount']
        image = args['image']

        product = Inventory(
            item = item,
            image = image,
            amount = amount
        )
        try:
            db.session.add(product)
            db.session.commit()
            id = product.id
            return ({
                'message': f"New inventory item added with ID: {id}",
                'item': {
                    'id': id,
                    'item': item,
                    'image': image,
                    'amount': amount
                }
            })
        except IntegrityError:
            db.session.rollback()
            return ({
                'message' : 'Item already exists or other error',
                }), 400

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item', type=str, required=True, help='Item name is required')
        parser.add_argument('amount', type=int, required=False, default = None)
        parser.add_argument('image', type=str, required=False, default= None)
        args = parser.parse_args()

        item = args['item']
        amount = args['amount']
        image = args['image']

        updated = {}

        if amount is not None:
            updated['amount'] = amount
        if image is not None:
            updated['image'] = image

        if updated:
            flag = Inventory.query.filter_by(item=item).update(updated)
            if flag == 1:
                db.session.commit()
                return ({
                    'message' : f'{item} updated!'
                    }), 200
        else:
            return ({
                'message' : 'Item doesn\'t exist or other error'
                }), 404

    def delete(self, item):

        flag = Inventory.query.filter_by(item=item).delete()
        if flag == 1:
            db.session.commit()
            return ({
                'message' : f'{item} deleted!'
                }), 200
        else:
            return ({
                'message' : 'Item doesn\'t exist or other error'
                }), 404

UPLOAD_FOLDER = os.path.join('/home/kegsouth/static', 'public', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def upload_file():
    if 'image' not in request.files:
        return ({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return ({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('uploaded_file', filename=filename, _external=True)
        item_id = request.form.get('item_id')
        print(f'Item ID: {item_id}')
        if item_id is None or item_id == '':
            return ({'error': 'Invalid item ID'}), 400
        item = Inventory.query.get(item_id)
        if item:
            item.image = image_url
            db.session.commit()
            return ({'message': 'File uploaded successfully', 'imageUrl': image_url}), 200
        else:
            return ({'error': 'Item not found'}), 404

    return ({'error': 'Invalid file type'}), 400


class Image_API(Resource):
    def post(self):
        return upload_file()



api.add_resource(Inventory_API, '/', '/<string:item>')
api.add_resource(Image_API, '/upload')


if __name__ == '__main__':
    app.run(debug=True)
