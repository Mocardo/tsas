from twitter_handler import TwitterHandler
from gcp_handler import GcpHandler

if __name__ == "__main__":
  # lê input da command line, que vai ser UMA key ou a frase "TT".
  twitter_key = input('type a keyword or "TT": ')

  # Invoca a api do twitter.
  twitter_handler_mode = (TwitterHandler.Mode.KEYWORD if twitter_key != 'TT'
    else TwitterHandler.Mode.TT)
  tweets_list = TwitterHandler.get_tweets(twitter_key, mode=twitter_handler_mode)

  # Invoca a api do google
  sentiment = GcpHandler.analyze_tweet(tweets_list)

  # Printa o resultado anterior.
  print(str(sentiment))
  