from marshmallow import Schema, fields


class LaunchProcessInputSchema(Schema):
    track = fields.List(fields.String(), required=True)


class LaunchProcessOutputSchema(Schema):
    process_started = fields.Boolean(required=True)


class StatisticsSchema(Schema):
    amount = fields.Int(required=True)
    elapsed_time = fields.Int(required=True)
    speed = fields.Float(required=True)
