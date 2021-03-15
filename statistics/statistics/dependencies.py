from nameko import config
from nameko.extensions import DependencyProvider
import redis


REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:

    def __init__(self, client):
        self.client = client

    def get(self, key: str):
        return self.client.get(key).decode("utf-8")

    def set(self, key: str, value):
        self.client.mset({key: value})
        return value


class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)
