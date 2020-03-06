import mongomock
import pytest
import simple_mongo

FIND_MOCK = [{'id': 1, 'name': 'Subratho', 'email': 's@gmail.com', 'contact': 9856237111, 'password': 's@123'}, {'id': 1, 'name': 'Subratho', 'email': 's@gmail.com', 'contact': 9856237111, 'password': 's@123'}, {'id': 1, 'name': 'Subratho', 'email': 's@gmail.com', 'contact': 9856237111, 'password': 's@123'}, {'id': 1, 'name': 'Subratho', 'email': 's@gmail.com', 'contact': 9856237111, 'password': 's@123'}, {'id': 1, 'name': 'Subratho', 'email': 's@gmail.com', 'contact': 9856237111, 'password': 's@123', 'address': 'sadgsahdfgf'}, {'id': None, 'name': None, 'email': None, 'contact': None, 'password': 'strisadadssaddasng', 'sdsad': 'ad'}]

class CalculatorStub:
    def addition(self):
        return 12
    
    def substraction(self):
        return 8
    


def test_get_simple_sum(mocker):
    mocker.patch("simple_mongo.get_random", side_effect=[1,2])
    result  = simple_mongo.get_simple_sum()
    assert result == 3

def get_mongo_stub():
    client = mongomock.MongoClient()
    db = client['test']
    db['test'].insert_one({})
    return client

@pytest.mark.parametrize("mongo_client, exp_response",[
({}, {}),
(None, None)
])
def test_get_connection_pass(mocker, mongo_client, exp_response):
    mocker.patch("pymongo.MongoClient", return_value=mongo_client)
    client = simple_mongo.get_connection()
    assert client == exp_response

def test_db_and_col_exists(mocker):
    client = get_mongo_stub()
    mocker.patch("simple_mongo.get_connection", return_value=client)
    result = simple_mongo.db_and_col_exists("test", "test")
    assert result




def test_insert_data(mocker):
    """
    funcion to insert data
    :param data:
    :return success:
    """
    client = get_mongo_stub()
    mocker.patch("simple_mongo.get_connection", return_value=client)
    result = simple_mongo.insert_data('test','test', {})
    assert result


@pytest.mark.parametrize("db_exist, find, exp_resp",[
(True, FIND_MOCK, FIND_MOCK),
(False, None, [])
])
def test_fetch_data(mocker, db_exist, find, exp_resp):
    mocker.patch('simple_mongo.db_and_col_exists',  return_value=db_exist)
    mocker.patch('pymongo.collection.Collection.find', return_value=find)
    result = simple_mongo.fetch_data('authentication','users')
    assert result == exp_resp




















def test_calculate_add(mocker):
    mocker.patch('simple_mongo.Calculator', return_value=CalculatorStub())
    result = simple_mongo.calculate_add(10, 2)
    assert result == 28