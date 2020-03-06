from flask import Flask
from flask_restplus import Api,Resource, fields


app = Flask(__name__)
api = Api(app)

#model
a_language =  api.model('Language', {'language': fields.String('The language')})


languages = []
python = {'language':'Python','id': 1}
languages.append(python)

@api.route('/languages')
class Language(Resource):

    @api.marshal_with(a_language,envelope='the_data')
    def get(self):
        return languages
    @api.expect(a_language)
    def post(self):
        new_lang = api.payload
        new_lang['id']  = len(languages) + 1
        languages.append(api.payload)
        return {'result':'Language added'}, 201

if __name__ == '__main__':
    app.run(debug=True)