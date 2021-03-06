import uvicorn
import pymongo
import pickle
import json
import time
from .sign import verify

secretkey = b'secretkey1234567890'
mongo = {}


def mongoinit(uri):
    global mongo
    mongo = pymongo.MongoClient(uri)


async def app(scope, receive, send):
    headers = dict(scope['headers'])
    body = await read_body(receive)
    signature = headers.get(b'signature', b'')

    #pylint: disable-msg=too-many-arguments
    if not verify(body, signature, secretkey):
        return await errorresponse(send, 'Unauthorized')

    data = json.loads(body)

    obj = mongo[data.get('db')][data.get('coll')]
    func = getattr(obj, data.get('func'))
    s = time.time()

    try:
        result = func(*data.get('args'), **data.get('kwargs'))
    except Exception as e:
        return await errorresponse(send, str(e))

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


async def read_body(receive):
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def errorresponse(send, msg):
    await send({
        'type': 'http.response.start',
        'status': 400,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': msg.encode('utf-8')
    })
    return None
