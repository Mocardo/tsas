from twitter_handler import TwitterHandler
from gcp_handler import GcpHandler

if __name__ == "__main__":
  twitter_key = input('Type a subject. Leave empty to use the main trending topic: ')

  # Call twiter API
  twitter_handler = TwitterHandler()
  tweets_list = twitter_handler.get_tweets(twitter_key)
  
  for tweet in tweets_list:
    print(tweet)
    print()

  # Invoca a api do google
  sentiment = GcpHandler.analyze_tweet(tweets_list)

  # Printa o resultado anterior.
  print(str(sentiment))
  