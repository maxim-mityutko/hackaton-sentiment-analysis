# Hackaton - Sentiment Analysis

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
Bash command to download the tweets:
```
 search_tweets.py --max-results 1500 --results-per-call 100 --filter-rule "lang:en #superrep #nike" --filename-prefix superrep --print-stream --credential-file config.yaml
```

## AWS Lambda
Download external libraries into lambda function folder for deployment via zip file
```
pip install requests -t .
pip install vaderSentiment -t .
pip install urllib3 -t .

zip -r sentiment-analysis.zip *
```
