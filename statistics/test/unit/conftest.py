import pytest
import redis

from nameko import config
from statistics.dependencies import REDIS_URI_KEY


@pytest.fixture
def test_config(rabbit_config):
    with config.patch(
        {REDIS_URI_KEY: 'redis://localhost:6379/11'}
    ):
        yield


@pytest.yield_fixture
def redis_client(test_config):
    client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))
    yield client
    client.flushdb()


@pytest.fixture
def create_param(redis_client):
    def create(key, value):
        redis_client.mset({key: value})
        return value
    return create


@pytest.fixture
def params(create_param):
    return [
        create_param(
            key='foo_1',
            value='bar_1',
        ),
        create_param(
            key='foo_2',
            value='bar_2',
        ),
        create_param(
            key='foo_3',
            value='bar_3',
        ),
    ]
