import pandas as pd
import random

from numpy.linalg import norm

import authorization
import numpy as np
from math import sqrt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("valence_arousal_dataset.csv")

df["mood_vector"] = df[['valence', 'energy']].values.tolist()

API = authorization.authorize()


def distance(point_1, point_2):
    return sqrt((point_2[0] - point_1[0])**2 + (point_1[1] - point_2[1])**2)


def recommend(track_id, number_of_records=5):
    track_features = API.track_audio_features(track_id)
    track_mood_vector = np.array([track_features.valence, track_features.energy])
    df["distance"] = df["mood_vector"].apply(lambda x: norm(track_mood_vector - np.array(x)))
    df_sorted = df.sort_values(by="distance", ascending=True)
    df_sorted = df_sorted[df_sorted["id"] != track_id]
    return df_sorted[["genre", "name", "artist", "distance"]][:number_of_records]


