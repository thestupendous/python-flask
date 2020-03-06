import pytest
import simple_apis
from test import test_data
from flask import Flask
app = Flask(__name__)


@pytest.fixture
def ctx():
    ctx = app.test_request_context()
    ctx.push()
    return ctx


def test_get_user(mocker, ctx):
    mocker.patch('flask_restplus.reqparse.RequestParser.parse_args', return_value={'limit':1})
    mocker.patch('simple_apis.fetch_data', return_value=test_data.FETCH_DATA)
    mocker.patch('simple_apis.marshal', return_value=test_data.MARSHAL)
    result = simple_apis.User().get()
    print(result)
    assert result[0] == test_data.GET_RESPONSE
    assert result[1] == 200


def test_post_user(mocker, ctx):
    mocker.patch('simple_apis.request.get_json', return_value=test_data.POST_USER)
    mocker.patch('simple_apis.marshal', return_value=test_data.POST_MARSHAL)
    mocker.patch('simple_apis.insert_data')
    result = simple_apis.User().post()
    assert result[0] == test_data.POST_RESPONSE
    assert result[1] == 201