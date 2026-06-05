import pandas as pd
import numpy as np

tracks_metadata = pd.read_csv('H:/KNN_recomendation/fma_metadata/fma_metadata/raw_tracks.csv')
print(tracks_metadata.columns)

def select_tracks_by_ids(ids):
    tracks_urls = []
    for id in ids:
        tracks_metadata_row = tracks_metadata[tracks_metadata['track_id'] == int(id)]
        if not tracks_metadata_row.empty:
            track_url = tracks_metadata_row['track_url'].values[0]
            tracks_urls.append(track_url)
    return tracks_urls