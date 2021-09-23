import requests
import os
import base64


class TwitterHandler:
  def __init__(self):
    _api_key = os.environ.get("API_KEY")
    _api_key_secret = os.environ.get("API_KEY_SECRET")

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

    _headers = {"Authorization": self.__bearer_token}
    payload = {
      'query': self.main_trend_topic() if keyphrase == '' else keyphrase,
      'max_results': 100 if max_results > 100 else max_results
    }
    response = requests.get('https://api.twitter.com/2/tweets/search/recent', params=payload,
                             headers=_headers)

    tweets = [data['text'] for data in response.json()['data']]
    return tweets


  def main_trend_topic(self):
    return "Arvore" # TODO: implement to get the main trending topic
