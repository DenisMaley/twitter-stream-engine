from nameko.testing.services import worker_factory

from listener.service import ListenerService


def test_start_stream():
    service = worker_factory(ListenerService)
    track = ['foo', 'bar']
    assert service.start_stream(track) == {'track': track}
