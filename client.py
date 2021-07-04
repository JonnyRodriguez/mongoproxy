import requests
import pickle
import json
from .sign import sign


class collection:
    def __init__(self, name, db):
        self.name = name
        self.db = db

    def __getattr__(self, name):
        self.func = name
        return getattr(self, '_func')

    def _func(self, *args, **kwargs):
        data = json.dumps({'db': self.db.name, 'coll': self.name, 'func': self.func,
                           'args': args, 'kwargs': kwargs})
        headers = {'signature': sign(data.encode('utf-8'))}

        response = requests.post(
            self.db.client.uri, data=data, headers=headers)

        if(response.status_code != 200):
            raise RuntimeError(response.text)

        return pickle.loads(response.content)


class db:
    def __init__(self, name, client):
        self.client = client
        self.name = name

    def __getitem__(self, name):
        return collection(name, self)

    def __getattr__(self, name):
        return collection(name, self)


class client:
    def __init__(self, uri):
        self.uri = uri

    def __getitem__(self, name):
        return db(name, self)

    def __getattr__(self, name):
        return db(name, self)
