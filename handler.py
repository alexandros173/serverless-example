import json
import logging
import os

import boto3


def create_currency(event, context):
    data = json.loads(event['body'])
    if ('symbol' or 'rate') not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the currency item.")

    dynamodb_client = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'symbol': data['symbol'],
        'rate': data['rate']
    }

    dynamodb_client.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response


def delete_currency(event, context):
    dynamodb_client = boto3.resource('dynamodb').Table('currency')

    dynamodb_client.delete_item(
        Key={
            'symbol': event['pathParameters']['symbol']
        }
    )

    return {"statusCode": 200}
