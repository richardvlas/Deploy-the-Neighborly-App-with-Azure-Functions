import json
import logging

import azure.functions as func


def main(event: func.EventHubEvent):
    body = event.get_body().decode()
    logging.info(f"Function triggered to process a message: {body}")

    result = json.loads(body)        
    logging.info(f'Python EventHub trigger processed an event: {result}')
