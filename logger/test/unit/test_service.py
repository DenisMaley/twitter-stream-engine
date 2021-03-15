from nameko.testing.services import worker_factory


from logger.service import LoggerService


def test_log_records(tmpdir):
    service = worker_factory(LoggerService)
    file = tmpdir.join('log.json')
    service.log_records(['foo', 'bar'], file)
    assert file.read() == '["foo", "bar"]'
