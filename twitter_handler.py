import requests
import base64
import json


class TwitterHandler:
  def __init__(self):
    f = open('secrets/twitter_api_key.json')
    _twitter_api_key = json.load(f)
    f.close()

    _api_key = _twitter_api_key.API_KEY
    _api_key_secret = _twitter_api_key.API_KEY_SECRET

    _credentials = _api_key + ":" + _api_key_secret
    _credentials_base64 = base64.b64encode(_credentials.encode('ascii'))
    _basic_token = "Basic " + _credentials_base64.decode('ascii')

    _headers = {
      "Authorization": _basic_token,
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    body = "grant_type=client_credentials"

    _response = requests.post('https://api.twitter.com/oauth2/token', headers=_headers, data=body)

    self.__bearer_token = "Bearer " + _response.json()["access_token"]


  def get_tweets(self, keyphrase='', max_results=10):
    """
    Returns a list of the last max_results tweets containing the specified keyphrase.
    If no keyphrase is specified, it will be the main trending topic.
    If max_results is greater than 100, it will only return 100.
    """

    if keyphrase == '':
      keyphrase = self.main_trend_topic()
      print("Using the folowing trend topic: " + keyphrase + "\n\n")

    _headers = {"Authorization": self.__bearer_token}
    payload = {
      'query': keyphrase,
      'max_results': 100 if max_results > 100 else max_results
    }
    response = requests.get('https://api.twitter.com/2/tweets/search/recent', params=payload,
                             headers=_headers)

    if response.json()['meta']['result_count'] == 0:
      return []  
    
    tweets = [data['text'] for data in response.json()['data']]
    return tweets


  def main_trend_topic(self):
    _headers = {"Authorization": self.__bearer_token}
    payload = {
      'id': 23424768, # Worldwide: 1 UK: 23424975 Brazil: 23424768 Germany: 23424829 Mexico: 23424900 Canada: 23424775 United States: 23424977 New York: 2459115
      'exclude': "%23"
    }
    response = requests.get('https://api.twitter.com/1.1/trends/place.json', params=payload,
                             headers=_headers)

    trend_topics = []
    for data in response.json()[0]['trends']:
      trend_topics.append( ( 0 if data['tweet_volume'] is None else data['tweet_volume'],
                             data['name']) )

    return trend_topics[0][1]
