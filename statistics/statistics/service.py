from nameko.rpc import rpc
from nameko.events import event_handler

from statistics import dependencies


class StatisticsService:

    name = 'statistics'
    storage = dependencies.Storage()

    @event_handler("listener", "log_statistics")
    def update_statistics(self, statistics: dict):
        for key, value in statistics.items():
            self.storage.add(key, value)

    @rpc
    def get_statistics(self):
        amount = int(float(self.storage.get('amount') or 0))
        elapsed_time = int(float(self.storage.get('elapsed_time') or 0))

        try:
            speed = amount / elapsed_time
        except ZeroDivisionError:
            speed = 0

        return {
            'amount': amount,
            'elapsed_time': elapsed_time,
            'speed': speed
        }
