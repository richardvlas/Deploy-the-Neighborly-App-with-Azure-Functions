import azure.functions as func
import logging
import os
import pymongo


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python createAdvertisement HTTP trigger function processed a request.')

    request = req.get_json()
    print(request)
    
    if request:
        try:
            url = os.environ['DbConnectionString']
            client = pymongo.MongoClient(url)
            database = client['mongodb1379128']
            collection = database['advertisements']

            rec_id1 = collection.insert_one(eval(request))

            return func.HttpResponse(req.get_body())                
        
        except Exception as e:
            logging.error(e)
            return func.HttpResponse("Database connection error.", status_code=500)
    
    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
        )
