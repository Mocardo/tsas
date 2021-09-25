# Twitter Sentiment Analyzer Service

A containerized service for inferring the sentiments of tweets by topic.

> ⚠️ You will need a [Twitter API key](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) placed in a `secrets/twitter_api_key.json` file like below:
> ```json
> {
>   "API_KEY": "<your twitter api key>",
>   "API_KEY_SECRET": "<your twitter api key secret>"
> }
> ```

> ⚠️ You will also need to [generate your own Google Cloud key](https://cloud.google.com/natural-language/docs/setup) and put the resulting json file in the secrets folder as well.

## Build
```sh
docker build -t tsas/csi-02-tsas .
```

## Run
Without cache:
```sh
docker run -ti tsas/csi-02-tsas
```

Saving cache:
```
docker run -ti -v `pwd`/caches:/usr/src/app/caches tsas/csi-02-tsas
```