from authorization import authorize
import pandas as pd
from tqdm import tqdm
import time

# Spotify API authorization
api = authorize()

# Genres fetching
genres = api.recommendation_genre_seeds()
num_of_songs_per_genre = 100

# Song object
songs = {
    "id": [],
    "genre": [],
    "name": [],
    "artist": [],
    "album": [],
    "valence": [],
    "energy": [],
    "acousticness": [],
    "danceability": [],
    "duration_ms": [],
    "instrumentalness": [],
    "key": [],
    "liveness": [],
    "loudness": [],
    "mode": [],
    "speechiness": [],
    "tempo": []
}

# iterates through ~120 genres
for genre in tqdm(genres):
    records = api.recommendations(genres=[genre], limit=num_of_songs_per_genre)
    records = eval(records.json().replace("null", "-999").replace("false", "False").replace("true", "True"))['tracks']

    # iterates through ~100 songs for specific genre and crawl the data
    for record in records:
        songs['id'].append(record['id'])
        songs['genre'].append(genre)

        songs['name'].append(record["name"])
        artists = [artist["name"] for artist in record["artists"]]
        songs['artist'].append(artists)
        songs['album'].append(record["album"]["name"])

        record_features = api.track_audio_features(record['id'])
        songs['valence'].append(record_features.valence)
        songs['energy'].append(record_features.energy)
        songs['acousticness'].append(record_features.acousticness)
        songs['danceability'].append(record_features.danceability)
        songs['duration_ms'].append(record_features.duration_ms)
        songs['instrumentalness'].append(record_features.instrumentalness)
        songs['key'].append(record_features.key)
        songs['liveness'].append(record_features.liveness)
        songs['loudness'].append(record_features.loudness)
        songs['mode'].append(record_features.mode)
        songs['speechiness'].append(record_features.speechiness)
        songs['tempo'].append(record_features.tempo)

        time.sleep(0.15)

df = pd.DataFrame(songs)
# removes duplicate songs and export dataset of the songs to csv file
df.drop_duplicates(subset='id', keep='first', inplace=True)
df.to_csv('final_dataset.csv', index=False)
