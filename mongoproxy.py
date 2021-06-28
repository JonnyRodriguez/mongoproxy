import requests
import pickle


class collection:
    def __init__(self, name, db):
        self.name = name
        self.db = db

    def __getattr__(self, name):
        self.func = name
        return getattr(self, '_func')

    def _func(self, *args, **kwargs):
        response = requests.post(self.db.client.uri, json={'db': self.db.name,
                                                           'coll': self.name,
                                                           'func': self.func,
                                                           'args': args,
                                                           'kwargs': kwargs})
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
