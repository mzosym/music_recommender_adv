from tekore import request_client_token, Spotify
from json import loads


def get_credentials(filename="credentials.txt"):
    credentials = loads(open(filename).read())
    return credentials['client_id'], credentials['client_secret']


def authorize():
    client_id, client_secret = get_credentials()
    token = request_client_token(client_id, client_secret)
    return Spotify(token)

