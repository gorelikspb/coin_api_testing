from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sys
from datetime import datetime
from time import time


def get_tickers(limit, sort):
    API_KEY = '0f9b82ba-c631-40ae-baf8-db9528b1edcd'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': limit,
        'convert': 'USD',
        'sort': sort  # 'volume_24h'

    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    return response


def metrics(response):
    output = {}
    start = time()
    res = (get_tickers(10, 'volume_24h'))
    output['req_time'] = time()-start
    output['status_code'] = res.status_code
    output['size'] = sys.getsizeof(res.text)
    json_data = json.loads(res.text)
    req_datetime_str = json_data['status']['timestamp']
    req_datetime_obj = datetime.strptime(
        req_datetime_str,  "%Y-%m-%dT%H:%M:%S.%fZ")
    request_date = (req_datetime_obj.date())
    today = (datetime.today().date())
    if request_date == today:
        output['actual'] = True
    else:
        output['actual'] = False

    if output['status_code'] == 200 and output['req_time'] < 0.5 and output['size'] < 10000 and output['actual']:
        output['passed'] = True
    else:
        output['passed'] = False
    return output


if __name__ == "__main__":

    res = get_tickers(10, 'volume_24h')
    metrics = metrics(res)
    if metrics['passed']:
        print('The test was successful')
    else:
        print('The test was failed')

    print('response status code:', metrics['status_code'])
    print('response time:', int(metrics['req_time']*1000),  'ms')
    print('data size:', metrics['size'], 'bytes')
    if metrics['actual']:
        print('Timestamp is actual')
    else:
        print('Timestamp is not actual')
