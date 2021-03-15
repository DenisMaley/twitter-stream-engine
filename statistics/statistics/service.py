from typing import Any
from nameko.rpc import rpc
from nameko.events import event_handler
from nameko_redis import Redis


class StatisticsService:

    name = 'statistics'
    redis = Redis('development')

    @event_handler("listener", "log_records")
    def update_statistics(self, records: list):
        self.set_param('amount', len(records))

    def set_param(self, key: str, value: Any):
        self.redis.set(key, value)
        return value

    @rpc
    def get_param(self, key: str):
        return self.redis.get(key)
