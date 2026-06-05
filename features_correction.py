import pandas as pd
import numpy as np

def get_correct_features():
    features = pd.read_csv('H:/KNN_recomendation/fma_metadata/fma_metadata/features.csv')

    features = features[3:]

    features= features.rename(columns={'feature': 'id'})

    features_values = features.values.astype(np.float64)

    print(features_values)

    return features_values

get_correct_features()