import pymongo
from calculator import Calculator

def get_connection():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017', socketTimeoutMS=12000)
    return client


def db_and_col_exists(database, collection):
    """
    funcion to check whether db and collection exists
    :param database:
    :param collection:
    :return exists:
    """
    exists = False
    client = get_connection()
    if database in client.list_database_names() and collection in client[database].list_collection_names():
        exists = True
    
    return exists


def insert_data(database,collection, data):
    """
    funcion to insert data
    :param data:
    :return success:
    """
    client = get_connection()
    success = client[database][collection].insert_one(data)
    return success

def fetch_data(database, collection, filter={}, projection={'_id':0}):
    """
    funcion to get data
    :param database:
    :param collection:
    :param filter:
    :return records:
    """
    client = get_connection()
    if not db_and_col_exists(database, collection):
        return []
    records = client[database][collection].find(filter, projection)
    return list(records)



def update(database, collection, data, id):
    client = get_connection()

    print(client[database][collection].update_one({"id":id},{"$set":data}))
    return True


def delete(database, collection, id):
    client = get_connection()
    doc_id = client[database][collection].delete({'id':id})
    return {'msg': str(doc_id)+' is deleted successfully'}


def get_random():
    import random
    return random.random()

def get_simple_sum():
    aa  = get_random() + get_random()
    return aa
    

def calculate_add(a,b):
    cal =  Calculator(a, b)
    result = cal.addition()+cal.substraction()+cal.substraction()
    return result
