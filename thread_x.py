from requests_oauthlib import OAuth1Session
import os
import json

# Suas chaves de autenticação
consumer_key = "eQhsfqVFbVZzMyqBv5jNw6aCe" #API Key
consumer_secret = "qdWYwiNq7IelRklTYcwGI0Ko9nohg5kB6kY3DQOZbZxZ4BoI8O"

# Obtenção do token de acesso - já presente no seu código
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


# Função para postar um tweet
def post_tweet(oauth, text, in_reply_to_tweet_id=None):
    payload = {"text": text}
    if in_reply_to_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": in_reply_to_tweet_id}
    
    print(payload)
    print(in_reply_to_tweet_id)

    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )
    
    if response.status_code != 201:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    
    json_response = response.json()
    return json_response

# Lista de tweets para a thread
tweets = [
    "Este é o início da thread no Twitter.",
    "Este é o segundo tweet da thread.",
    "Aqui está o terceiro tweet da nossa thread.",
    "Finalmente, o último tweet da thread!"
]

# Publicando os tweets em uma thread
previous_tweet_id = None
for tweet_text in tweets:
    response_data = post_tweet(oauth, tweet_text, in_reply_to_tweet_id=previous_tweet_id)
    previous_tweet_id = response_data["data"]["id"]  # Captura o ID do último tweet para referenciar o próximo

    print(json.dumps(response_data, indent=4, sort_keys=True))

print("Thread publicada com sucesso!")
