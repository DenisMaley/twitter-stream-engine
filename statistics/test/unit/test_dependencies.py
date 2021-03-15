import pytest
from mock import Mock

from nameko import config
from statistics.dependencies import Storage


@pytest.fixture
def storage(test_config):
    provider = Storage()
    provider.container = Mock(config=config)
    provider.setup()
    return provider.get_dependency({})


@pytest.mark.skip(reason="connection to Redis needs to be fixed")
def test_get(storage, params):
    param = storage.get('foo_1')
    assert 'bar_1' == param


@pytest.mark.skip(reason="connection to Redis needs to be fixed")
def test_create(product, redis_client, storage):

    storage.set(key='test_key', value='test_value')

    stored_param = redis_client.get('test_key')

    assert stored_param.decode('utf-8') == 'test_value'
