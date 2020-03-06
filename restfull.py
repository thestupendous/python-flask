from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class defaultroute(Resource):
    def get(self):
        return {'dskfl':'sdkfj'}
    def post(self):
        jdata = request.get_json()
        return {'got data ':jdata}, 201

class newnew(Resource):
    def get(self,num):
        return {'default route ':num*30}

api.add_resource(defaultroute,'/')
api.add_resource(newnew,'/newnew/<int:num>')

app.run(debug=True)