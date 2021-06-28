import uvicorn
from dotenv import load_dotenv
from os import environ
import pymongo
import pickle
import json
import time


load_dotenv()
mongo = pymongo.MongoClient(environ.get('mongouri'))


async def read_body(receive):
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def app(scope, receive, send):
    data = json.loads(await read_body(receive))
    print(data)

    obj = mongo[data.get('db')][data.get('coll')]
    func = getattr(obj, data.get('func'))

    s = time.time()
    result = func(*data.get('args'), **data.get('kwargs'))

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })

    if(isinstance(result, pymongo.cursor.Cursor)):
        result = list(result)

    await send({
        'type': 'http.response.body',
        'body': pickle.dumps(result)
    })
    print(time.time()-s)
