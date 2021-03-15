from nameko.testing.services import worker_factory

from listener.service import ListenerService, format_message


class DictX(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'


message = DictX({
    'id': '1',
    'id_str': '1',
    'created_at': '12431241234',
    'text': 'test',
    'user': DictX({
        'id': 1,
        'screen_name': '@name'
    })
})


def test_format_message():
    assert format_message(message) == {
        'id': message.id_str,
        'creation_timestamp': message.created_at,
        'text': message.text,
        'author_id': message.user.id,
        'author_name': message.user.screen_name
    }


def test_on_status():
    service = worker_factory(ListenerService)
    service.on_status(message)
    assert len(service.tweets_list) == 1


def test_on_connect():
    service = worker_factory(ListenerService)
    service.on_connect()
    assert service.start_moment > 0


def test_on_error():
    service = worker_factory(ListenerService)
    assert not service.on_error(420)


def test_log_trigger():
    service = worker_factory(ListenerService)
    service.log_trigger()
    assert service.start_moment > 0
