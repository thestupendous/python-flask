import json
from flask import Flask, make_response, request
# import PayloadValidator
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
import simple_mongo
from simple_mongo import insert_data, fetch_data, update, delete

DATABASE = 'authentication'
COLLECTION = 'users'

NS = Namespace('User API', description='User API Version 2.0')
NS1 = Namespace('User API with id', description='User API with id Version 2.0')

APP = Flask(__name__)

QUERY_FILTERS = reqparse.RequestParser()
QUERY_FILTERS.add_argument('limit', type=int, help="limit  - only integer values allowed")
# QUERY_FILTERS.add_argument('name', type=str, help="name  - only string values allowed")
USER_MODEL = NS.model('user',
    {
        "id" : fields.Integer(required=True, description="Id of the user"),
        "name": fields.String(required=True, description = "Name of the user"),
        "email": fields.String(required=True, description = "Email of the user"),
        "contact": fields.Integer(required=True, description="Contact of the user"),
        "password": fields.String(required=True, description="Password of the user")
    }
)

USER_LIST = NS.model('user list', 
{ 
    "users": fields.List(fields.Nested(USER_MODEL), description = "list of users")
}
)


SIMPLE_RESPONSE = NS.model('simple_response',
    {
        "id" : fields.Integer(required=True, description="Id of the user"),
        "name": fields.String(required=True, description = "Name of the user")
    }
)

@NS.response(200, 'Success', SIMPLE_RESPONSE)
@NS.response(400, 'BAD REQUEST', SIMPLE_RESPONSE)
@NS.route("/user")
class User(Resource):
    @NS.doc(params={'limit': 'required parameter indicating the limit of the users to retrieve', 'name':'required parameter indicating the limit of the users to retrieve'})
    def get(self):
        filters = QUERY_FILTERS.parse_args()
        print(filters)
        data = {}
        data['users'] = fetch_data(DATABASE, COLLECTION)[0:filters['limit']]
        
        data = marshal(data, USER_LIST)

        return data, 200


    @NS.expect(USER_MODEL, validate=True)
    def post(self):
        data = request.get_json()
        data = marshal(data, USER_MODEL)
        
        insert_data(DATABASE, COLLECTION, data)
        del data['_id']
        return data, 201



# @NS.response(200, 'Success', SIMPLE_RESPONSE)
@NS1.route("/user/<id>")
class UserId(Resource):
    def get(self, id):
        return {'id':id}, 200
    
    @NS1.expect(USER_MODEL)
    def put(self, id):
        data = request.get_json()
        data = marshal(data, USER_MODEL)
        update(DATABASE, COLLECTION, data, int(id))
        return data, 200


    def delete(self, id):
        resp = delete(DATABASE, COLLECTION, id)
        return resp, 204

