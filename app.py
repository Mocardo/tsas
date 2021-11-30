from typing import List, Tuple, Union
from flask import Flask, escape, request, jsonify

from gcp_handler import AnalysisSummary, GcpHandler, TweetSentiment,\
  POSITIVE_LABEL, NEGATIVE_LABEL, NEUTRAL_LABEL

from twitter_handler import TwitterHandler
import utils

app = Flask(__name__)

@app.route('/api/summary')
def summary():
  q = request.args.get('q', None)
  if q is None:
    return query_invalida()
  q = escape(q)

  analysis_result = call_apis(q)
  summ = make_summary(analysis_result)

  return jsonify({'summary': summ})

@app.route('/api/list')
def list():
  q = request.args.get('q', None)
  if q is None:
    return query_invalida()
  q = escape(q)

  analysis_result = call_apis(q)

  return jsonify({'list': analysis_result})
    
@app.route('/api/sumlist')
def summary_and_list():
  q = request.args.get('q', None)
  if q is None:
    return query_invalida()
  q = escape(q)

  analysis_result = call_apis(q)
  summ = make_summary(analysis_result)

  return jsonify({'list': analysis_result, 'summary': summ})

def query_invalida() -> Tuple[str, int]:
  return "query invalida" , 400

def call_apis(q: str) -> List[TweetSentiment]:
  twitter_handler = TwitterHandler()
  tweet_list = twitter_handler.get_tweets(q)
  #utils.cache_json(tweet_list, 'tweets')

  gcp_handler = GcpHandler()
  sentiments = gcp_handler.analyze_tweets(tweet_list)
  #utils.cache_json(sentiments, 'tweet_sentiments')

  return sentiments

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
