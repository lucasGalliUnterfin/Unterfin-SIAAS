import os
from dotenv import load_dotenv
import tweepy

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../..", "claves.env"))
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise RuntimeError("No se encontró TWITTER_BEARER_TOKEN en claves.env")


client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

def fetch_last_tweets(username: str):

    # Obtiene el objeto usuario para su ID interno
    user = client.get_user(username=username).data
    if not user:
        raise RuntimeError(f"Usuario @{username} no encontrado")

    # Solicita solo 5 tweets
    resp = client.get_users_tweets(
        id=user.id,
        max_results=5,
        tweet_fields=["created_at", "text", "id"],
    )
    tweets = resp.data or []

    return [{
        "date": t.created_at,
        "id": t.id,
        "content": t.text,
        "url": f"https://twitter.com/{username}/status/{t.id}"
    } for t in tweets]


# Testing
username = "Deltaone"
tweets = fetch_last_tweets(username)
if not tweets:
    print(f"No se encontraron tweets para @{username}.")
else:
    print(f"Últimos {len(tweets)} tweets de @{username}:\n")
    for t in tweets:
        print(f"{t['date']} — {t['content']}\n  {t['url']}\n")

"""
Rate limit exceeded. Sleeping for 743 seconds.
Traceback (most recent call last):
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connection.py", line 516, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 1395, in getresponse
    response.begin()
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 325, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 294, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\util\retry.py", line 474, in increment
    raise reraise(type(error), error, _stacktrace)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\util\util.py", line 38, in reraise
    raise value.with_traceback(tb)
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\urllib3\connection.py", line 516, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 1395, in getresponse
    response.begin()
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 325, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\http\client.py", line 294, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\resea\OneDrive\Escritorio\Unterfin-SIAAS\src\ingestion\tweets.py", line 38, in <module>
    tweets = fetch_last_tweets(username)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\resea\OneDrive\Escritorio\Unterfin-SIAAS\src\ingestion\tweets.py", line 21, in fetch_last_tweets
    resp = client.get_users_tweets(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\tweepy\client.py", line 1593, in get_users_tweets
    return self._make_request(
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\tweepy\client.py", line 129, in _make_request
    response = self.request(method, route, params=request_params,
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\tweepy\client.py", line 113, in request
    return self.request(method, route, params, json, user_auth)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\tweepy\client.py", line 84, in request
    with self.session.request(
         ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\resea\AppData\Local\Programs\Python\Python311\Lib\site-packages\requests\adapters.py", line 682, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
"""