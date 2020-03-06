from flask import Flask
from flask_restplus import Api
from simple_apis import NS as simple_namespace
from simple_apis import NS1
app = Flask(__name__)
api = Api(app, version='1.0', title='Authentication API',
          description='Authentication API')

api.add_namespace(simple_namespace, path="/authentication")
api.add_namespace(NS1, path="/authentication")

if __name__ == '__main__':
   app.run(debug = True)



