# Twitter Sentiment Analyzer Service

A containerized service for inferring the sentiments of tweets by topic.

## Code and architecture
The implementation is explained on [code_description.md](code_description.md).

## Service usage
The service was deployed on heroku [csi02-tsas.herokuapp.com](https://csi02-tsas.herokuapp.com/).

There are six routes:

- `/api/list`: returns a list of tweets for the #1 Trend Topic with their sentiment analysis.
- `/api/list/<topic>`: returns a list of tweets for the given topic with their sentiment analysis.
- `/api/sumlist`: returns a list of tweets for the #1 Trend Topic with their sentiment analysis and a summary of that sentiment analysis.
- `/api/sumlist/<topic>`: returns a list of tweets for the given topic with their sentiment analysis and a summary of that sentiment analysis.
- `/api/summary`: returns just a summary of the sentiment analysis of the #1 Trend Topic.
- `/api/summary/<topic>`: returns just a summary of the sentiment analysis of the given topic.

The complete API documentation is available at [https://csi02-tsas.herokuapp.com/](https://csi02-tsas.herokuapp.com/).

## Running the service

> ⚠️ You will need a [Twitter API key](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) placed in a `secrets/twitter_api_key.json` file like below:
> ```json
> {
>   "API_KEY": "<your twitter api key>",
>   "API_KEY_SECRET": "<your twitter api key secret>"
> }
> ```

> ⚠️ You will also need to [generate your own Google Cloud key](https://cloud.google.com/natural-language/docs/setup) and put the resulting json file in the secrets folder as well.

### 1. Build
```sh
docker build -t tsas/csi-02-tsas .
```

### 2. Run
Without cache:
```sh
docker run -p 8000:8000 -ti tsas/csi-02-tsas
```

Saving cache:
```
docker run -p 8000:8000 -ti -v `pwd`/caches:/usr/src/app/caches tsas/csi-02-tsas
```

So you can access the service locally on [localhost:8000](localhost:8000).
