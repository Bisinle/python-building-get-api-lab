#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list =[]
    for bakery in bakeries:
        bakery_dict = {
            'id':bakery.id,
            'name': bakery.name,
            'created_at':bakery.created_at,
            'updated_at':bakery.updated_at
        }
        bakeries_list.append(bakery_dict)

    return make_response(jsonify(bakeries_list),200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    bakery_data = bakery.to_dict()
    print(bakery_data)
    # bakery_data = {
    #     'name' : bakery.name,
    #     'created_at' : bakery.created_at,
    #     'updated_at':bakery.updated_at
    # }
 
    return make_response(jsonify(bakery_data,))


 

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
     baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
     baked_goods_list = []
     for bakery_good in baked_goods:
        baked_goods_dict = {
            'id':bakery_good.id,
            'name':bakery_good.name,
            'created_at':bakery_good.created_at,
            'updated_at':bakery_good.updated_at,
            'bakery_id':bakery_good.bakery_id,
            'price':bakery_good.price
        }
        baked_goods_list.append(baked_goods_dict)
     return make_response(jsonify(baked_goods_list),200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()
    
    
    most_expensive_dict = most_expensive.to_dict()
    return make_response(most_expensive_dict,200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
