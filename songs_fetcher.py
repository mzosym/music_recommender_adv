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
    "valence": [],
    "energy": []
}
# iterates through ~120 genres
for genre in tqdm(genres):
    records = api.recommendations(genres=[genre], limit=num_of_songs_per_genre)
    records = eval(records.json().replace("null", "-999").replace("false", "False").replace("true", "True"))['tracks']

    # iterates through ~100 songs for specific genre and crawl the data
    for record in records:
        songs['id'].append(record['id'])
        songs['genre'].append(genre)

        record_meta = api.track(record['id'])
        songs['name'].append(record_meta.name)
        songs['artist'].append(record_meta.album.artists[0].name)

        record_features = api.track_audio_features(record['id'])
        songs['valence'].append(record_features.valence)
        songs['energy'].append(record_features.energy)

        time.sleep(0.15)

df = pd.DataFrame(songs)
# removes duplicate songs and export dataset of the songs to csv file
df.drop_duplicates(subset='id', keep='first', inplace=True)
df.to_csv('valence_arousal_dataset.csv', index=False)
