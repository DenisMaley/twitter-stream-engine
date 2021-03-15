from nameko.rpc import rpc
from nameko.events import event_handler

from statistics import dependencies


class StatisticsService:

    name = 'statistics'
    storage = dependencies.Storage()

    @event_handler("listener", "log_records")
    def update_statistics(self, records: list):
        self.storage.set('amount', len(records))

    @rpc
    def get_statistics(self):
        return self.storage.get('amount')
