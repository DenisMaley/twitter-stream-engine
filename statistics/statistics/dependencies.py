from nameko import config
from nameko.extensions import DependencyProvider
import redis


REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:

    def __init__(self, client):
        self.client = client

    def add(self, key: str, value: float):
        value += float(self.get(key) or 0)
        self.set(key, value)

    def get(self, key: str):
        value = self.client.get(key)
        if value:
            value = value.decode("utf-8")
        return value

    def set(self, key: str, value):
        self.client.set(key, value)
        return value


class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)
