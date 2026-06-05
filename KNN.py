import numpy as np

class KNN:
    def __init__(self):
        pass

    def get_neighbours(self, playlist, current, k): #формат - только NP массив с id и фичами
        distances = []
        for i in range(len(playlist)):
            id = playlist[i][0]
            distance = np.linalg.norm(playlist[i][1:] - current)
            distances.append([id, distance])
        
        distances = np.array(distances)
        distances = distances[distances[:,1].argsort()][:k]
        return distances
    

