import os
import json
from typing import Union
from nameko.events import event_handler


class LoggerService:

    name = 'logger'

    @event_handler("listener", "log_records")
    def log_records(
            self,
            records: list,
            file: Union[str, bytes, os.PathLike] = 'log.json'
    ):
        with open(file, 'w') as log_file:
            log_file.write(json.dumps(records))
