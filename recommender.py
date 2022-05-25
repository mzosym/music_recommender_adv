import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm

df = pd.read_csv("valence_arousal_dataset.csv")
print(df.shape)
df.head()