import json
import logging

currency_map = dict()


def consume_topic(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        symbol = message['data']['symbol']
        if message['type'] == 'INSERT' or message['type'] == 'MODIFY':
            currency_map[symbol] = message['data']['rate']

        if message['type'] == 'REMOVE':
            currency_map.pop(symbol) if symbol in currency_map else logger.info(f'symbol: {symbol} not in map')

        logger.info(f'currency map: {currency_map}')
