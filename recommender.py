import pandas as pd
from numpy.linalg import norm
import authorization
import numpy as np

# option to show all columns in the dataset
pd.set_option('display.max_columns', None)
# read the dataset
df = pd.read_csv("final_dataset.csv")
# instead of separate mood values set a vector of them for simplicity
df["mood_vector"] = df[['valence', 'energy']].values.tolist()
# authorize
API = authorization.authorize()


def recommend_by_mood(track_id, number_of_records=5):
    # get searching track features
    track_features = API.track_audio_features(track_id)
    # get this track mood vector
    track_mood_vector = np.array([track_features.valence, track_features.energy])
    # calculate the distance to this track from every other in the dataset
    df["distance"] = df["mood_vector"].apply(lambda x: norm(track_mood_vector - np.array(x)))
    if track_mood_vector[0] >= 0.5 and track_mood_vector[1] >= 0.75:
        df["danceability_distance"] = track_features.danceability - df["danceability"]
        # sort by less distance and similar by danceability
        df_sorted = df.sort_values(by=["distance", "danceability_distance"], ascending=True)
        df_sorted = df_sorted[(df_sorted["distance"] > 0.02) & (df_sorted["distance"] < 0.2) &
                              (df_sorted["danceability_distance"] > 0)]
    elif track_mood_vector[0] <= 0.2 and track_mood_vector[1] <= 0.1:
        df["acousticness_distance"] = track_features.acousticness - df["acousticness"]
        # sort by less distance and similar by acousticness
        df_sorted = df.sort_values(by=["distance", "acousticness_distance"], ascending=True)
        df_sorted = df_sorted[(df_sorted["distance"] > 0.02) & (df_sorted["distance"] < 0.2) &
                              (df_sorted["acousticness_distance"] > 0)]
    else:
        # sort by less distance
        df_sorted = df.sort_values(by=["distance"], ascending=True)
    # remove the source track from the list, if it was there
    df_sorted = df_sorted[df_sorted["id"] != track_id]
    # return first n tracks that are similar by the mood to the source one
    return df_sorted[["genre", "name", "artist", "distance", "danceability_distance"]][:number_of_records]