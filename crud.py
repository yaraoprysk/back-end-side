import copy
import json

from flask import Flask, request, jsonify, abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin, CORS

from models.abstract_product import AbstractProduct

with open('secret.json') as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"])

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class SmartAbstractProduct(AbstractProduct, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variety = db.Column(db.String(32), unique=False)
    capacity = db.Column(db.Integer, unique=False)
    packing = db.Column(db.String(32), unique=False)
    producer = db.Column(db.String(32), unique=False)
    roasting = db.Column(db.String(32), unique=False)
    price = db.Column(db.Integer(), unique=False)

    def __init__(self, variety, capacity, packing, producer,
                 roasting, price):
        super().__init__(variety, capacity, packing, producer,
                         roasting, price)


class SmartAbstractProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'variety', 'capacity',
                  'packing', 'producer',
                  'roasting', 'price')


smart_abstract_product_schema = SmartAbstractProductSchema()
smart_abstract_products_schema = SmartAbstractProductSchema(many=True)


@app.route("/coffee", methods=["POST"])
@cross_origin()
def add_smart_abstract_product():
    variety = request.json['variety']
    capacity = request.json['capacity']
    packing = request.json['packing']
    producer = request.json['producer']
    roasting = request.json['roasting']
    price = request.json['price']
    smart_abstract_product = SmartAbstractProduct(
        variety,
        capacity,
        packing,
        producer,
        roasting,
        price
    )
    db.session.add(smart_abstract_product)
    db.session.commit()

    response = smart_abstract_product_schema.jsonify(smart_abstract_product)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/coffee", methods=["GET"])
def get_smart_abstract_product():
    all_smart_abstract_product = SmartAbstractProduct.query.all()
    result = smart_abstract_products_schema.dump(all_smart_abstract_product)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/coffee/<id>", methods=["GET"])
@cross_origin()
def smart_abstract_product_detail(id):
    smart_abstract_product = SmartAbstractProduct.query.get(id)
    if not smart_abstract_product:
        abort(404)
    response = smart_abstract_product_schema.jsonify(smart_abstract_product)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/coffee/<id>", methods=["PUT"])
@cross_origin()
def smart_abstract_product_update(id):
    smart_abstract_product = SmartAbstractProduct.query.get(id)
    if not smart_abstract_product:
        abort(404)
    old_smart_abstract_product = copy.deepcopy(smart_abstract_product)
    smart_abstract_product.variety = request.json['variety']
    smart_abstract_product.capacity = request.json['capacity']
    smart_abstract_product.packing = request.json['packing']
    smart_abstract_product.producer = request.json['producer']
    smart_abstract_product.roasting = request.json['roasting']
    smart_abstract_product.price = request.json['price']
    db.session.commit()
    response = smart_abstract_product_schema.jsonify(smart_abstract_product)
    return response


@app.route("/coffee/<id>", methods=["DELETE"])
def smart_abstract_product_delete(id):
    smart_abstract_product = SmartAbstractProduct.query.get(id)
    if not smart_abstract_product:
        abort(404)
    db.session.delete(smart_abstract_product)
    db.session.commit()
    response = smart_abstract_product_schema.jsonify(smart_abstract_product)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    db.create_all()
    app.run(debug=False, host='localhost')