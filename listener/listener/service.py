import time

from collections import defaultdict

from nameko import config
from nameko.rpc import rpc
from nameko.events import EventDispatcher

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from resettabletimer import ResettableTimer


TIME_LIMIT = 30  # seconds
AMOUNT_LIMIT = 100


def format_message(message):
    return {
        'id': message.id_str,
        'creation_timestamp': message.created_at,
        'text': message.text,
        'author_id': message.user.id,
        'author_name': message.user.screen_name,
    }


class ListenerService(StreamListener):

    name = 'listener'
    dispatch = EventDispatcher()

    def __init__(self):
        StreamListener.__init__(self)
        self.tweets_list = defaultdict(list)
        self.timer = ResettableTimer(TIME_LIMIT, self.log_trigger)
        self.start_moment = 0

    def on_connect(self):
        self.timer.start()
        self.start_moment = time.time()

    def on_status(self, status):
        tweet = format_message(status)

        self.tweets_list[tweet['author_id']].append(tweet)
        if len(self.tweets_list) == AMOUNT_LIMIT:
            self.log_trigger()

        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

    @rpc
    def start_stream(self, track: list):
        auth = OAuthHandler(
            config.get('CONSUMER_KEY'), config.get('CONSUMER_SECRET')
        )
        auth.set_access_token(
            config.get('ACCESS_TOKEN'), config.get('ACCESS_TOKEN_SECRET')
        )
        stream = Stream(auth, self)

        stream.filter(track=track, is_async=True)

        return True

    @rpc
    def log_trigger(self):

        elapsed_time = time.time() - self.start_moment

        self.dispatch('log_records', self.tweets_list)
        self.dispatch(
            'log_statistics',
            {
                'amount': len(self.tweets_list),
                'elapsed_time': elapsed_time
            }
        )

        self.tweets_list = defaultdict(list)
        self.timer.reset()
        self.start_moment = time.time()
