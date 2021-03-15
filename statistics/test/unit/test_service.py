import pytest

from nameko.testing.services import entrypoint_hook

from statistics.service import StatisticsService


@pytest.fixture
def service_container(test_config, container_factory):
    container = container_factory(StatisticsService)
    container.start()
    return container


@pytest.mark.skip(reason="connection to Redis needs to be fixed")
def test_update_get_statistics(service_container):
    with entrypoint_hook(service_container, 'update_statistics') as \
            update_statistics:
        update_statistics(['a', 's', 'd'])

        with entrypoint_hook(service_container, 'get_statistics') as \
                get_statistics:
            amount = get_statistics()

    assert amount == 3
