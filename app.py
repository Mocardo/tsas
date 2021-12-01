from typing import List, Tuple, Union
from flask import Flask, jsonify
from flask_restx import Resource, Api, fields

from gcp_handler import AnalysisSummary, GcpHandler, TweetSentiment,\
  POSITIVE_LABEL, NEGATIVE_LABEL, NEUTRAL_LABEL

from twitter_handler import TwitterHandler
import utils

app = Flask(__name__)
api = Api(app, version='1.0', title='TSAS',
          description='A Twitter Sentiment Analysis Service.\n\
              Here you can find out the sentiment of a given topic or even the #1 Trend Topic in Brazil.')
ns = api.namespace('api', description='Default API')


tweet_sentiment_model = ns.model("TweetSentiment", {
    'identified_lang': fields.String(description='Identified language'),
    'score': fields.Float(description='Sentiment score'),
    'sentiment': fields.String(description='Inferred sentiment'),
    'tweet_text': fields.String(description='Tweet text')
})

analysis_summary_model = ns.model("AnalysisSummary", {
    'negative_percentage': fields.Float(description='Percentage of negative tweets'),
    'neutral_percentage': fields.Float(description='Percentage of neutral tweets'),
    'positive_percentage': fields.Float(description='Percentage of positive tweets')
})

list_model = ns.model('SentimentList', {
    "list": fields.List(fields.Nested(tweet_sentiment_model)),
    "topic": fields.String(description='Desired topic')
})

summary_model = ns.model("Summary", {
    'summary': fields.Nested(analysis_summary_model),
    'topic': fields.String(description='Desired topic')
})

sumlist_model = ns.model("SummaryAndList", {
    'list': fields.List(fields.Nested(tweet_sentiment_model)),
    'summary': fields.Nested(analysis_summary_model),
    'topic': fields.String(description='Desired topic')
})

@ns.route('/summary', defaults={'topic': ""},
            doc={'description': 'Get the sentiment analysis summary of the #1 Trend Topic.'})
@ns.route('/summary/<path:topic>',
            doc={'description': 'Get the sentiment analysis summary of a given topic.'})
class summary(Resource):
  @ns.response(200, 'Success', summary_model)
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    if '/' in topic:
      return 'Invalid query', 400

    topic = topic.strip()

    analysis_result, top  = call_apis(topic)
    summ = make_summary(analysis_result)

    return jsonify({'topic': top,
                    'summary': summ.to_dict()})


@ns.route('/list', defaults={'topic': ""},
            doc={'description': 'Get a list of tweets, with their sentiment analysis, for the #1 Trend Topic.'})
@ns.route('/list/<path:topic>',
            doc={'description': 'Get a list of tweets, with their sentiment analysis, for a given topic.'})
class list(Resource):
  @ns.response(200, 'Success', list_model)
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    if '/' in topic:
      return 'Invalid query', 400

    topic = topic.strip()

    analysis_result, top = call_apis(topic)

    return jsonify({'topic': top,
                    'list': utils.list_to_list_of_dicts(analysis_result)})


@ns.route('/sumlist', defaults={'topic': ""},
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for the #1 Trend Topic.'})
@ns.route('/sumlist/<path:topic>',
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for a given topic.'})
class summary_and_list(Resource):
  @ns.response(200, 'Success', sumlist_model)
  @ns.response(400, 'Invalid query')
  def get(self, topic):
    if '/' in topic:
      return 'Invalid query', 400

    topic = topic.strip()

    analysis_result, top = call_apis(topic)
    summ = make_summary(analysis_result)

    return jsonify({'topic': top,
                    'list': utils.list_to_list_of_dicts(analysis_result),
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
