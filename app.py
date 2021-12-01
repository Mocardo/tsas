from typing import List, Tuple, Union
from flask import Flask, escape, request, jsonify
from flask_restx import Resource, Api

from gcp_handler import AnalysisSummary, GcpHandler, TweetSentiment,\
  POSITIVE_LABEL, NEGATIVE_LABEL, NEUTRAL_LABEL

from twitter_handler import TwitterHandler
import utils

app = Flask(__name__)
api = Api(app, version='1.0', title='TSAS',
          description='A Twitter Sentiment Analysis Service.\n\
              Here you can find the sentiment of a given topic or even the #1 Trend Topic in Brazil.')
ns = api.namespace('api', description='Default API')

@ns.route('/api/summary', defaults={'topic': ""},
            doc={'description': 'Get the sentiment analysis summary of the #1 Trend Topic.'})
@ns.route('/api/summary/<topic>',
            doc={'description': 'Get the sentiment analysis summary of a given topic.'})
class summary(Resource):
  @ns.response(200, 'Success')
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    topic = topic.strip()

    analysis_result, top  = call_apis(topic)
    summ = make_summary(analysis_result)

    return jsonify({'topic': top,
                    'summary': summ.to_dict()})


@ns.route('/api/list', defaults={'topic': ""},
            doc={'description': 'Get a list of tweets, with their sentiment analysis, for the #1 Trend Topic.'})
@ns.route('/api/list/<topic>',
            doc={'description': 'Get a list of tweets, with their sentiment analysis, for a given topic.'})
class list(Resource):
  @ns.response(200, 'Success')
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    topic = topic.strip()

    analysis_result, top = call_apis(topic)

    return jsonify({'topic': top,
                    'list': utils.sentiment_list_to_dict(analysis_result)})


@ns.route('/api/sumlist', defaults={'topic': ""},
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for the #1 Trend Topic.'})
@ns.route('/api/sumlist/<topic>',
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for a given topic.'})
class summary_and_list(Resource):
  @ns.response(200, 'Success')
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    topic = topic.strip()
    
    analysis_result, top = call_apis(topic)
    summ = make_summary(analysis_result)

    return jsonify({'topic': top,
                    'list': utils.sentiment_list_to_dict(analysis_result),
                    'summary': summ.to_dict()})


def query_invalida() -> Tuple[str, int]:
  return "Invalid query" , 400

def call_apis(q: str) -> Tuple[List[TweetSentiment], str]:
  twitter_handler = TwitterHandler()
  tweet_list, topic = twitter_handler.get_tweets(q)
  #utils.cache_json(tweet_list, 'tweets')

  gcp_handler = GcpHandler()
  sentiments = gcp_handler.analyze_tweets(tweet_list)
  #utils.cache_json(sentiments, 'tweet_sentiments')

  return sentiments, topic

def make_summary(analysis: List[TweetSentiment]) -> Union[AnalysisSummary, None]:
  num_positive = 0
  num_negative = 0
  num_neutral = 0

  for tweet in analysis:
    if tweet.sentiment == POSITIVE_LABEL:
      num_positive += 1
    elif tweet.sentiment == NEGATIVE_LABEL:
      num_negative += 1
    else:
      num_neutral += 1

  total_tweets = len(analysis)
    
  if total_tweets > 0:
    return AnalysisSummary(100*num_positive/total_tweets, 
                           100*num_negative/total_tweets,
                           100*num_neutral/total_tweets)
  else:
    return None
