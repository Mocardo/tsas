# Twitter Sentiment Analyzer Service

> ⚠️ You will need a Twitter API key placed in a secrets/twitter_api_key.json file like below:
> ```json
> {
>   "API_KEY": "<your twitter api key>",
>   "API_KEY_SECRET": "<your twitter api key secret>"
> }
> ```

> ⚠️ You will also need to generate your own Google Cloud key as shown at https://cloud.google.com/natural-language/docs/setup, put the resulting file in secrets folder as well.

## Build
```sh
docker build -t tsas/csi-02-tsas .
```

## Run
```sh
sudo docker run -ti tsas/csi-02-tsas
```
