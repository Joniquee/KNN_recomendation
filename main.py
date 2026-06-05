from PCA_class import PCA
import features_correction
from KNN import KNN
from features import get_correct_features
import numpy as np
from track_selection import select_tracks_by_ids

def main():
    pca = PCA(n_components=300)
    features = features_correction.get_correct_features()
    pca.fit(features)
    features = pca.transform(features)
    #print('Sigma values:', pca.get_sigma())
    print('Information rate: {:.2f}%'.format(pca.information_rate() * 100))

    path = 'H:/KNN_recomendation/Crystal_Castles_-_Crimewave_(SkySound.cc).mp3'
    new_id = max(features[:,0])
    cur_track = get_correct_features(path)
    cur_track = np.c_[[new_id], cur_track]
    cur_track = pca.transform(cur_track)
    knn = KNN()
    print(f'features shape = {features.shape}, current shape = {cur_track.shape}')
    closest = knn.get_neighbours(features, cur_track, 3)
    print(closest)

    urls = select_tracks_by_ids(closest[:, 0])
    print(urls)

if __name__ == "__main__":
    main()
