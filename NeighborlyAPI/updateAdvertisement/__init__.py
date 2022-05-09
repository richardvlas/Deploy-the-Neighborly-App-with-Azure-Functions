import azure.functions as func
import logging
import os
import pymongo
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python updateAdvertisement HTTP trigger function processed a request.')

    id = req.params.get('id')
    request = req.get_json()
    
    if request:
        try:
            url = os.environ['DbConnectionString']
            client = pymongo.MongoClient(url)
            database = client['mongodb1379128']
            collection = database['advertisements']

            filter_query = {'_id': ObjectId(id)}
            update_query = {"$set": eval(request)}
            rec_id1 = collection.update_one(filter_query, update_query)

            return func.HttpResponse(status_code=200)                
        
        except Exception as e:
            logging.error(e)
            print("WHAT THE FUCK")
            return func.HttpResponse("Database connection error.", status_code=500)
    
    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
        )
