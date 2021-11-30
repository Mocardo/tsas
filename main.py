from twitter_handler import TwitterHandler, Tweet
from gcp_handler import GcpHandler
from datetime import datetime
import json

# para entregar, setar as duas como False
CACHE_FOLDER = 'caches'
GCP_DEBUG = False
TWI_DEBUG = False

def cache_json(obj, fname_beg):
  obj_str = json.dumps(obj, indent=2, default=lambda o: o.__dict__)
  path = CACHE_FOLDER + f'/{fname_beg}_{datetime.now()}.json'
  cax = open(path, 'w')
  cax.write(obj_str)
  cax.close()

if __name__ == "__main__":
  # Caso estejamos debugando somente uma api, melhor não chamar a outra pra
  # evitar custos.
  if not GCP_DEBUG:
    twitter_key = input('Type a subject. Leave empty to use the main trending topic: ')
    # Call twiter API
    twitter_handler = TwitterHandler()
    tweet_list = twitter_handler.get_tweets(twitter_key)
    
    cache_json(tweet_list, 'tweets')

  else:
    cax = open('caches/tweets.json', 'r')
    tweet_list = [Tweet(txt) for txt in json.load(cax)]
    cax.close()

  if not TWI_DEBUG:
    gcp_handler = GcpHandler()
    # Invoca a api do google
    sentiments = gcp_handler.analyze_tweets(tweet_list)

    cache_json(sentiments, 'tweet_sentiments')
    
    #print(u'{}'.format(sen_json))

    score_positive = 0
    score_negative = 0
    score_neutral = 0

    for sent in sentiments:
      if sent.score > 0:
        score_positive += 1
        sent.score = 'POSITIVE'
      elif sent.score < 0:
        score_negative += 1
        sent.score = 'NEGATIVE'
      else:
        score_neutral += 1
        sent.score = 'NEUTRAL'
      
      delattr(sent, "identified_lang")
    
    cache_json(sentiments, 'analysis')

    #print(u'{}'.format(ana_json))
    total_tweets = score_positive + score_negative + score_neutral
    
    if len(sentiments) > 0:
      print("Percentual positivo: {}%".format(100*score_positive/total_tweets))
      print("Percentual negativo: {}%".format(100*score_negative/total_tweets))
      print("Percentual neutro/não identificado: {}%".format(100*score_neutral/total_tweets))
    else:
      print("NENHUM TWEET")
