from typing import Any
import pytest
from redis import StrictRedis


def test_key_plugin():
    return 'nameko-test-value'


def pytest_configure():
    pytest.test_key = test_key_plugin()


@pytest.fixture
def redis_db(request: Any):
    url = 'redis://redis:6379/1'

    def redis_teardown():
        client = StrictRedis.from_url(url)
        client.delete(pytest.test_key)
    request.addfinalizer(redis_teardown)
    return url
