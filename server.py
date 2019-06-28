# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 16:47:01 2019

@author: luigi de lisi
"""
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify

db_crypto = create_engine('sqlite:///crypto.db')
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

############
class CryptoUsd(Resource):
    
    def get(self):
        conn = db_crypto.connect()
        query = conn.execute("SELECT * FROM data1")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class CryptoEur(Resource):
    
    def get(self):
        conn = db_crypto.connect()
        query = conn.execute("SELECT * FROM data2")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class CryptoGbp(Resource):
    
    def get(self):
        conn = db_crypto.connect()
        query = conn.execute("SELECT * FROM data3")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(CryptoUsd, '/crypto/USD')
api.add_resource(CryptoEur, '/crypto/EUR')
api.add_resource(CryptoGbp, '/crypto/GBP')


if __name__ == '__main__':
     app.run(port='5002')