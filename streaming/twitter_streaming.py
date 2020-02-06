import json

from tweepy import OAuthHandler, API, StreamListener, Stream
import boto3
import logging
import streaming.conf as conf

search_string = '<<SEARCH_CONDITION>>'

logger = logging.getLogger(__name__)


# Twitter client
def init_client(client_id: str, client_secret: str, token: str, token_secret: str) -> API:
    auth = OAuthHandler(client_id, client_secret)
    auth.set_access_token(token, token_secret)
    return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Stream Listener
class TwitterStreamListener(StreamListener):
    def on_status(self, status):
        tweet = status._json
        logger.info(tweet)

        # Push data to Kinesis stream
        kinesis.put_record(
            DeliveryStreamName='twitter-stream',
            Record={'Data': 'b' + json.dumps(tweet)}
        )

        # Push data to S3 bucket
        s3.put_object(
            Body=json.dumps(tweet, indent=2),
            Bucket='nike-hackathon-2020',
            Key='raw/{}.json'.format(tweet['id_str'])
        )


client = init_client(
    client_id=conf.twitter['client_id'],
    client_secret=conf.twitter['client_secret'],
    token=conf.twitter['token'],
    token_secret=conf.twitter['token_secret'],
)

s3 = boto3.client('s3',
    aws_access_key_id=conf.aws['aws_access_key_id'],
    aws_secret_access_key=conf.aws['aws_secret_access_key'],
)

kinesis = boto3.client('firehose',
    aws_access_key_id=conf.aws['aws_access_key_id'],
    aws_secret_access_key=conf.aws['aws_secret_access_key'],
    region_name='eu-central-1'
)


listener = TwitterStreamListener()
stream = Stream(auth=client.auth, listener=listener)
stream.filter(track=[search_string], is_async=True)

