import json
import os

import boto3


def listen_currency(event, context):

    client = boto3.client('sns')
    for record in event.get('Records'):
        event_name = record.get('eventName')
        msg = {'type': event_name}
        if event_name in 'INSERT' or event_name in 'MODIFY':
            msg['data'] = {
                'symbol': record['dynamodb']['NewImage']['symbol']['S'],
                'rate': record['dynamodb']['NewImage']['rate']['S']
            }
        if event_name in 'REMOVE':
            msg['data'] = {
                'symbol': record['dynamodb']['Keys']['symbol']['S']
            }

        client.publish(TopicArn=os.environ['SNS_TOPIC'], Message=json.dumps(msg))
