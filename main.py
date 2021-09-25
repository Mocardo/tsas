from twitter_handler import TwitterHandler, Tweet
from gcp_handler import GcpHandler
from datetime import datetime
import json

# para entregar, setar as duas como False
GCP_DEBUG = False
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

    #print(u'{}'.format(tl_json))

  else:
    cax = open('caches/tweets.json', 'r')
    tweet_list = [Tweet(txt) for txt in json.load(cax)]
    cax.close()

  if not TWI_DEBUG:
    gcp_handler = GcpHandler()
    # Invoca a api do google
    sentiments = gcp_handler.analyze_tweets(tweet_list)

    sen_json = json.dumps(sentiments, indent=2, default=lambda obj: obj.__dict__)
    
    cax = open(f'caches/tweet_sentiments_{datetime.now()}.json', 'w')
    cax.write(sen_json)
    cax.close()

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
    
    ana_json = json.dumps(sentiments, indent=2, default=lambda obj: obj.__dict__)

    cax = open(f'caches/analysis_{datetime.now()}.json', 'w')
    cax.write(ana_json)
    cax.close()

    #print(u'{}'.format(ana_json))
    total_tweets = score_positive + score_negative + score_neutral
    if len(sentiments) > 0:
      print("Percentual positivo: {}%".format(100*score_positive/total_tweets))
      print("Percentual negativo: {}%".format(100*score_negative/total_tweets))
      print("Percentual neutro/não identificado: {}%".format(100*score_neutral/total_tweets))
    else:
      print("NENHUM TWEET")
