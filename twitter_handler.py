import requests
import base64
import json
from typing import List


class Tweet:
  def __init__(self, text: str, lang: str=None):
    self.text = text
    self.lang = lang


class TwitterHandler:
  def __init__(self):
    f = open('secrets/twitter_api_key.json')
    twitter_api_key = json.load(f)
    f.close()

    api_key = twitter_api_key["API_KEY"]
    api_key_secret = twitter_api_key["API_KEY_SECRET"]

    credentials = api_key + ":" + api_key_secret
    credentials_base64 = base64.b64encode(credentials.encode('ascii'))
    basic_token = "Basic " + credentials_base64.decode('ascii')

    headers = {
      "Authorization": basic_token,
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    body = "grant_type=client_credentials"

    response = requests.post('https://api.twitter.com/oauth2/token',
     headers=headers, data=body)

    self.__bearer_token = "Bearer " + response.json()["access_token"]


  def get_tweets(self, keyphrase:str='', max_results:int=10) -> List[Tweet]:
    """
    Returns a list of the last max_results tweets containing the specified
    keyphrase. If no keyphrase is specified, it will be the main trending
    topic. If max_results is greater than 100, it will only return 100.
    """

    if keyphrase == '':
      keyphrase = self.main_trend_topic()
      print("Using the folowing trend topic: " + keyphrase + "\n\n")

    headers = {"Authorization": self.__bearer_token}
    payload = {
      'query': keyphrase,
      'max_results': 100 if max_results > 100 else max_results,
      'tweet.fields': 'lang'
    }
    response = requests.get('https://api.twitter.com/2/tweets/search/recent',
     params=payload, headers=headers)

    #print(response.json())
    
    if response.json()['meta']['result_count'] == 0:
      return []
    
    tweet_list = [Tweet(data['text'], data['lang']) for data in response.json()['data']]
    # TODO: add language metadata for tweets (low priority)

    return tweet_list


  def main_trend_topic(self):
    headers = {"Authorization": self.__bearer_token}
    payload = {
      'id': 23424768, # Worldwide: 1 UK: 23424975 Brazil: 23424768
       # Germany: 23424829 Mexico: 23424900 Canada: 23424775
       # United States: 23424977 New York: 2459115
      'exclude': "%23"
    }
    response = requests.get('https://api.twitter.com/1.1/trends/place.json',
     params=payload, headers=headers)

    trend_topics = []
    for data in response.json()[0]['trends']:
      trend_topics.append( ( 0 if data['tweet_volume'] is None
       else data['tweet_volume'], data['name']) )

    return trend_topics[0][1]
