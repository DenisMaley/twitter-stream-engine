from nameko.rpc import rpc
from nameko.events import EventDispatcher


class ListenerService:

    name = 'listener'
    dispatch = EventDispatcher()

    @rpc
    def start_stream(self, track: list) -> object:
        return {'track': track}

    @rpc
    def log_trigger(self, records: list) -> None:
        self.dispatch('log_records', records)
