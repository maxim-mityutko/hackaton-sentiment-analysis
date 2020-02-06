# hackaton-sentiment-analysis

## Collect or stream Tweets
How to connect to Twitter: [Twitter API](https://developer.twitter.com/en/docs)
Scripts for batch download of tweets: [GIT - search-tweets-python](https://github.com/twitterdev/search-tweets-python) and example config:
```yaml
search_tweets_api:
  account_type: premium
  endpoint: https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json
  consumer_key: <<consumer_key>>
  consumer_secret: <<consumer_secret>>

```

## AWS Lambda
Download external libraries into lambda function folder for deployment via zip file
```
pip install requests -t .
pip install vaderSentiment -t .
pip install urllib3 -t .

zip -r sentiment-analysis.zip *
```
