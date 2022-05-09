import azure.functions as func
import logging
import os
import pymongo
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python deleteAdvertisement HTTP trigger function processed a request.')

    id = req.params.get("id")
        
    if id:
        try:
            url = os.environ['DbConnectionString']
            client = pymongo.MongoClient(url)
            database = client['mongodb1379128']
            collection = database['advertisements']

            query = {'_id': ObjectId(id)}
            result = collection.delete_one(query)
            return func.HttpResponse("")                
        
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
    
    else:
        return func.HttpResponse(
            "Please pass an id in the query string",
            status_code=400
        )
