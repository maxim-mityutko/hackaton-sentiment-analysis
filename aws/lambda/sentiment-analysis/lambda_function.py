import json
import boto3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Getting s3 object
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
              
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. '
              'Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    
    # Parse s3 object content (JSON)
    try:
        s3_file_content = response['Body'].read()
        # clean trailing comma
        if s3_file_content.endswith(b',\n'):
            s3_file_content = s3_file_content[:-2]
        tweets_str = '[' + s3_file_content.decode('utf-8') + ']'
        tweets = json.loads(tweets_str)
   
    except Exception as e:
        print(e)
        print('Error loading json from object {} in bucket {}'.format(key, bucket))
        raise e
    
    # Do the sentiment analysis
    try:
        sia = SentimentIntensityAnalyzer()
        tweet = tweets[0]
        sentiment = sia.polarity_scores(tweet['text'])
        payload = {
            'tweet': tweet,
            'sentiment': sentiment,
        }
        print(payload)
        s3.put_object(
            Bucket='nike-hackaton-2020',
            Key='processed/{}.json'.format(tweet['id_str']),
            Body=json.dumps(payload, indent=2),
        )
        ## DUMMY

    except Exception as e:
        print(e)
        print('Error loading data into ElasticSearch')
        raise e    


if __name__ == '__main__':
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {'name': 'nike-hackaton-2020'},
                    'object': {'key': 'raw'}
                }
            }
        ]
    }
    lambda_handler(event, None)

