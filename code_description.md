# Código e arquitetura do serviço

O serviço montado foca em fornecer ao usuário uma análise de sentimento a respeito de um determinado tópico, utilizando-se dos tweets mais recentes.

A aplicação está hospedada no Heroku, plataforma virtual que permite desenvolvedores hospedarem seus aplicativos em ambiente de nuvem.

Há, no servidor de serviços, uma aplicação no port 80 responsável por receber requests http, analisá-los e, caso não seja detectado nenhum erro de formato, respondê-los.

A aplicação fornece uma API simples de seis rotas que analisam sentimentos a respeito de determinado tópico no Twitter. As rotas diferem entre si no conteúdo forma que é retornado ao usuário a respeito do tópico pedido.

Os requests são em formato de mensagens GET, em que toda a informação passada ao servidor está contida diretamente na URI na forma de path parameters. Seus responses são em formato de mensagens HTTP com o corpo contendo um JSON, cujo formato há de ser entendido pelo usuário da API previamente.

Para alcançar todos esses resultados, toda a aplicação está dividida em duas partes: uma responsável por receber e responder requests, e outra responsável por coletar e analisar os tweets.

## Atendimento a requisições

As rotas são implementadas usando classes herdadas do `Resource` do `flask_restx`. Um exemplo de uma rota é a seguinte, que implementa a rota `/api/sumlist`:

```python
@ns.route('/sumlist', defaults={'topic': ""},
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for the #1 Trend Topic.'})
@ns.route('/sumlist/<path:topic>',
            doc={'description': 'Get a list of tweets, with their sentiment analysis, and a summary for a given topic.'})
class summary_and_list(Resource):
    @ns.response(200, 'Success', sumlist_model)
    @ns.response(400, 'Invalid query')
    def get(self, topic):
    if '/' in topic:
        return 'Invalid query', 400

    topic = topic.strip()

    analysis_result, top = call_apis(topic)
    summ = make_summary(analysis_result)

    return jsonify({'topic': top,
                    'list': utils.list_to_list_of_dicts(analysis_result),
                    'summary': summ.to_dict()})
```
Esse trecho do código, por exemplo, define o método `get` da classe como o handler de requests para essa rota, que na verdade aparece como duas pela ausência ou não do path parameter topic. Esse parâmetro é passado como um argumento para a função get, que passa ela para a parte do serviço que cuida da chamada das API's de terceiros. Por fim, quando essa parte retorna, o handler formata os dados num dict, que  é então convertido em seguida para JSON e enviado para o cliente.

## API's de terceiros

Cada uma rotas implementadas fazem uso das classes `TwitterHandler` e `GcpHandler` para realizar a análise de sentimento dos tweets.

### Obtendo os tweets
A classe `TwitterHandler` é usada para conversar com a API do Twitter e obter uma lista de tweets mais recentes de acordo com o tópico passado.
Seu método mais importante é o `get_tweets()`, que faz tal retorno. 

```python
def get_tweets(self, keyphrase:str='') -> Tuple[List[Tweet], str]:
    """
    Returns a pair with the list of the last 10 most popular tweets containing
    the specified keyphrase and with the topic queried. If no keyphrase is
    specified, it will be the main trending topic. If max_results is greater
    than 100, it will only return 100.
    """
    max_results = 100
    if keyphrase == '':
        keyphrase = self.main_trend_topic()
        print("Using the main trend topic: " + keyphrase + "\n\n")

    headers = {"Authorization": self.__bearer_token}
    payload = {
        'q': keyphrase,
        'count': 100 if max_results > 100 else max_results,
        'result_type': 'popular',
        'lang': 'pt'
    }
    response = requests.get('https://api.twitter.com/1.1/search/tweets.json',
    params=payload, headers=headers)
    if response.json()['search_metadata']['count'] == 0:
        return []

    tweet_list = [Tweet(data['text'], data['lang'], data['retweet_count'])
        for data in response.json()['statuses']]

    return (tweet_list, keyphrase)
```

### Analisando o sentimento dos tweets
Para analisar os sentimentos dos tweets, a classe `GcpHandler` usa a API do Google Cloud, passando como texto de analise, o texto dos tweets obtido anteriormente.
Seu método mais importante é o `analyze_tweet()` que junto com `_call_api()` retorna o sentimento do tweet.

```python
def analyze_tweets(self, tweet_list: List[Tweet]) -> List[TweetSentiment]:
    tweets_analysis = [] # Will store the function output
    
    for tweet in tweet_list:
        if tweet.lang in ["pt", "en", "es"]:
            response = self._call_api(tweet)

            tweets_analysis.append(TweetSentiment(
            tweet_text=tweet.text,
            score=response.document_sentiment.score,
            identified_lang=response.language
            ))
    return tweets_analysis

def _call_api(self, tweet: Tweet):
    request = {
      'document': {
        'content': tweet.text,
        'type_': language_v1.Document.Type.PLAIN_TEXT,
        'language': tweet.lang
      },
      'encoding_type': language_v1.EncodingType.UTF8
    }
    response = self.client.analyze_sentiment(request=request)
    return response
```
