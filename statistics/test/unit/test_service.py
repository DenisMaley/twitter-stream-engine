from typing import Any
import pytest
from nameko.testing.services import entrypoint_hook
from redis import StrictRedis

from statistics.service import StatisticsService
from nameko_redis import REDIS_URIS_KEY


@pytest.mark.skip(reason="connection to Redis needs to be fixed")
def test_set_get_param(container_factory: Any, redis_db: Any):
    config = {
        REDIS_URIS_KEY: {
            'development': redis_db
        },
        'AMQP_URI': "amqp://guest:guest@localhost:5672"
    }

    container = container_factory(StatisticsService, config)
    container.start()

    with entrypoint_hook(container, "set_param") as set_param:
        set_param(pytest.test_key, 'foo')

    client = StrictRedis.from_url(redis_db, decode_responses=True)
    assert client.get(pytest.test_key) == "foo"

    with entrypoint_hook(container, "get_param") as get_param:
        assert get_param(pytest.test_key) == "foobar"
