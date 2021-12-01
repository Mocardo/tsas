from typing import List
from twitter_handler import Tweet
from google.cloud import language_v1

POSITIVE_LABEL = 'POSITIVE'
NEGATIVE_LABEL = 'NEGATIVE'
NEUTRAL_LABEL = 'NEUTRAL/NOT_IDENTIFIED'


class TweetSentiment:
  def __init__(self, tweet_text: str, score: float, #magnitude: float,
   identified_lang: str):
    self.tweet_text = tweet_text
    self.score = score
    # self.magnitude = magnitude
    self.identified_lang = identified_lang
    if score > 0:
      self.sentiment = POSITIVE_LABEL
    elif score < 0:
      self.sentiment = NEGATIVE_LABEL
    else:
      self.sentiment = NEUTRAL_LABEL
  def to_dict(self):
    return self.__dict__


class AnalysisSummary:
  def __init__(self, pos_percent, neg_percent, ntr_percent):
    self.positive_percent = pos_percent
    self.negative_percent = neg_percent
    self.neutral_percent = ntr_percent
  def to_dict(self):
        return self.__dict__



class GcpHandler:
  def __init__(self):
    self.client = language_v1.LanguageServiceClient()

  def analyze_tweets(self, tweet_list: List[Tweet]) -> List[TweetSentiment]:
    tweets_analysis = [] # Will store the function output
    
    for tweet in tweet_list:
      if tweet.lang in ["pt", "en", "es"]:
        response = self._call_api(tweet)

        tweets_analysis.append(TweetSentiment(
          tweet_text=tweet.text,
          score=response.document_sentiment.score,
          #magnitude=response.document_sentiment.magnitude,
          identified_lang=response.language
        ))

    return tweets_analysis
      
  def _call_api(self, tweet: Tweet):
    # print(tweet.lang)
    request = {
      'document': {
        'content': tweet.text,
        'type_': language_v1.Document.Type.PLAIN_TEXT,
        'language': tweet.lang
        #'language': None
      },
      'encoding_type': language_v1.EncodingType.UTF8
    }
    response = self.client.analyze_sentiment(request=request)
    return response
