from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

## Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
# Initialize db
db = SQLAlchemy(app)

# Initialize Ma
ma = Marshmallow(app)


## Producr Class.Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description,price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

## Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields =('id', 'name', 'description', 'price','qty')



## Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)




#### Create EndPoints #####
## create a Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty'] 
 
    new_product = Product(name, description, price, qty)

    # add to db
    db.session.add(new_product)
    db.session.commit() #commit to database

    return product_schema.jsonify(new_product)

## Get All Products
@app.route('/product', methods=['GET'])
def get_products():
     #fetch all products
    all_products = Product.query.all()

    result = products_schema.dump(all_products) 
    return jsonify(result)


## Update a Product
@app.route('/product/<id>', methods=['PUT'])
def get_product(id):
    #fetch product
    product = Product.query.get(id) 

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty'] 

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()  #commit to db

    return product_schema.jsonify(product)

## Get Single Product
@app.route('/product/<id>', methods=['GET'])
def update_product(id):
     #fetch product
    product = Product.query.get(id) 

    return product_schema.jsonify(product)



## Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    #fetch product
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit() #commit to database

    return product_schema.jsonify(product)



## RUn server 
if __name__ == "__main__":
   #Keep our server running, set debu = true
   app.run(debug=True)