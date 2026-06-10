from PCA import PCA
from features_initiation import get_init_features
from KNN import KNN
from features import get_correct_features
import numpy as np
from track_selection import select_track_urls_by_ids, tracks_metadata
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import random
import queue
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv() 

TRACKS_PATH = os.getenv('TRACKS_PATH', 'H:/KNN_recomendation/fma_small/fma_small')

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/track_info/{track_id}')
def get_track_info(track_id: str):
    track_id = int(track_id.lstrip('0'))
    title  = tracks_metadata[tracks_metadata['track_id'] == track_id]['track_title'].values[0]
    artist = tracks_metadata[tracks_metadata['track_id'] == track_id]['artist_name'].values[0]
    image_url = tracks_metadata[tracks_metadata['track_id'] == track_id]['track_image_file'].values[0]
    return {'title': title, 'artist': artist, 'image_url': image_url}

@app.get('/audio/{track_id}')
def get_audio(track_id: str):
    folder = track_id[:3]
    path = f'{TRACKS_PATH}/{folder}/{track_id}.mp3'
    if not path.exists():
        raise HTTPException(status_code=404, detail="Track not found")
    return FileResponse(path, media_type='audio/mpeg')


pca = PCA(300)
features = get_init_features()
transformed_features = pca.fit_transform(features)

@app.get('/next_track')
def get_next_track(curent_track_id : str):
    id = curent_track_id
    id = id.lstrip('0')
    track_features = features[features[:, 0]== int(id)]
    track_features = pca.transform(track_features)
    knn = KNN()
    print(f'features shape = {transformed_features.shape}, current shape = {track_features.shape}')
    k = 3
    closest = knn.get_neighbours(transformed_features, track_features, k)
    print(closest)
    
    urls = select_track_urls_by_ids(closest[:, 0])
    rand_track = random.choice(urls)
    while rand_track[0] == int(id):
        rand_track = random.choice(urls)

    urls_d = {rand_track[0]: rand_track[1]}
    return urls_d #возвращает словарь с id трека и url трека в формате {id: url}

def main():
    get_next_track('051006')


if __name__ == "__main__":
    main()
