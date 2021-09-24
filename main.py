from twitter_handler import TwitterHandler, Tweet
from gcp_handler import GcpHandler
from datetime import datetime
import json

# para entregar, setar as duas como False
GCP_DEBUG = True
TWI_DEBUG = False

if __name__ == "__main__":
  # Caso estejamos debugando somente uma api, melhor não chamar a outra pra
  # evitar custos.
  if not GCP_DEBUG:
    twitter_key = input('Type a subject. Leave empty to use the main trending topic: ')
    # Call twiter API
    twitter_handler = TwitterHandler()
    tweet_list = twitter_handler.get_tweets(twitter_key)
    
    tl_json = json.dumps(tweet_list, indent=2, default=lambda obj: obj.__dict__)
    
    cax = open(f'caches/tweets_{datetime.now()}.json', 'w')
    cax.write(tl_json)
    cax.close()

    print(u'{}'.format(tl_json))

  else:
    cax = open('caches/tweets.json', 'r')
    # TODO relativamente importante: como fazer para os arquivos no caches
    # do docker virem pra pasta do projeto?
    tweet_list = [Tweet(txt) for txt in json.load(cax)]
    cax.close()

  if not TWI_DEBUG:
    gcp_handler = GcpHandler()
    # Invoca a api do google
    sentiment = gcp_handler.analyze_tweets(tweet_list)

    sen_json = json.dumps(sentiment, indent=2, default=lambda obj: obj.__dict__)
    
    cax = open(f'caches/tweet_sentiments_{datetime.now()}.json', 'w')
    cax.write(sen_json)
    cax.close()

    print(u'{}'.format(sen_json))
  