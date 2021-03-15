import json

from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response

from nameko.web.handlers import http
from gateway.schemas import (
    LaunchProcessInputSchema,
    LaunchProcessOutputSchema,
    StatisticsSchema
)


class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    listener_rpc = RpcProxy('listener')
    statistics_rpc = RpcProxy('statistics')

    @http("POST", "/launch")
    def launch_process(self, request):
        """Launch listening the stream - track data is posted as json

        Example request ::

            {
                "track": ["bieber"]
            }

        """

        schema = LaunchProcessInputSchema(strict=True)

        try:
            stream_params = schema.loads(request.get_data(as_text=True)).data
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc))

        # Create the product
        process_started = self.listener_rpc.start_stream(**stream_params)
        result = {'process_started': process_started}
        return Response(
            LaunchProcessOutputSchema().dumps(result).data,
            mimetype='application/json'
        )

    @http("GET", "/statistics")
    def get_statistics(self, request):
        statistics = self.statistics_rpc.get_statistics()
        return Response(
            StatisticsSchema().dumps(statistics).data,
            mimetype='application/json'
        )
