import azure.functions as func
import logging
import os
import pymongo
from bson.json_util import dumps


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python getPost HTTP trigger function processed a request.')

    id = req.params.get('id')

    if id:
        try:
            url = os.environ['DbConnectionString']
            client = pymongo.MongoClient(url)
            database = client['mongodb1379128']
            collection = database['posts']

            query = {'_id': str(id)}
            result = collection.find_one(query)
            result = dumps(result)

            return func.HttpResponse(
                result, mimetype="application/json", charset='utf-8', 
                status_code=200
            )
        except Exception as e:
            logging.error(e)
            return func.HttpResponse(
                "Database connection error.", status_code=500
            )
    
    else:
        return func.HttpResponse(
             "Please pass an id parameter in the query string.", 
             status_code=400
        )
