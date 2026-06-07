import pandas as pd
import numpy as np

tracks_metadata = pd.read_csv('H:/KNN_recomendation/fma_metadata/fma_metadata/raw_tracks.csv')
tracks_features = pd.read_csv('H:/KNN_recomendation/fma_metadata/fma_metadata/features.csv')
print(tracks_metadata.columns)

def select_track_urls_by_ids(ids):
    tracks_urls = []
    for id in ids:
        tracks_metadata_row = tracks_metadata[tracks_metadata['track_id'] == int(id)]
        if not tracks_metadata_row.empty:
            track_url = tracks_metadata_row[['track_id','track_url']].values[0]
            tracks_urls.append(track_url)
    return tracks_urls #возвращает список треков в формате [[id, url]]

def select_tracks_by_ids(ids):
    for id in ids:
        tracks_metadata_row = tracks_metadata[tracks_metadata['track_id'] == int(id)]
        if not tracks_metadata_row.empty:
            track_features = tracks_metadata_row.values[0]
    return track_features #возвращает фичи трека в формате [[id, features]]