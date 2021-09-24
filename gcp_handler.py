from typing import List
from twitter_handler import Tweet
from google.cloud import language_v1


class TweetSentiment:
  def __init__(self, tweet_text: str, score: float, #magnitude: float,
   identified_lang: str):
    self.tweet_text = tweet_text
    self.score = score
    # self.magnitude = magnitude
    self.identified_lang = identified_lang


class GcpHandler:
  def __init__(self):
    self.client = language_v1.LanguageServiceClient()

  def analyze_tweets(self, tweet_list: List[Tweet]) -> List[TweetSentiment]:
    tweets_analysis = [] # Will store the function output
    
    for tweet in tweet_list:
      response = self._call_api(tweet)

      tweets_analysis.append(TweetSentiment(
        tweet_text=tweet.text,
        score=response.document_sentiment.score,
        #magnitude=response.document_sentiment.magnitude,
        identified_lang=response.language
      ))

    return tweets_analysis
      
  def _call_api(self, tweet: Tweet):
    request = {
      'document': {
        'content': tweet.text,
        'type_': language_v1.Document.Type.PLAIN_TEXT,
        'language': tweet.lang
      },
      'encoding_type': language_v1.EncodingType.UTF8
    }
    response = self.client.analyze_sentiment(request=request)
    return response
