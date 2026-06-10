import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

FEATURES_CSV = os.getenv('FEATURES_CSV')

def get_init_features():
    features = pd.read_csv(FEATURES_CSV)

    features = features[3:]

    features= features.rename(columns={'feature': 'id'})

    features_values = features.values.astype(np.float64)

    return features_values #возвращаются фичи с id в np массиве

