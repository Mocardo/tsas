# Twitter Sentiment Analyzer Service

> ⚠️ You will need a Twitter API key placed in a twitter_api_key.py file like below:
> ```python
> API_KEY = '<your twitter api key>'
> API_KEY_SECRET = 'your twitter api key secret'
> ```

> ⚠️ You will also need to generate your own Google Cloud key as shown at https://cloud.google.com/natural-language/docs/setup

## Build
```sh
docker build -t ocimar/csi-02-tsas .
```

## Run
```sh
sudo docker run -ti ocimar/csi-02-tsas
```
