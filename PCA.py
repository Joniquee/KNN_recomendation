import numpy as np
from sklearn.preprocessing import StandardScaler



class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
    

    def fit(self, X): #X - NP массив с id и фичами
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X[:, 1:])

        U, Sigma, VT = np.linalg.svd(X_scaled, full_matrices=False)

        self.full_Sigma = Sigma.copy()

        for i in range(self.n_components, len(Sigma)): # выделение главных сингулярных чисел матрицы
            Sigma[i] = 0

        self.VT = VT
        self.Sigma = Sigma
        
    def information_rate(self):
        return np.sum(self.Sigma[:self.n_components]) / np.sum(self.full_Sigma)
    
    def transform(self, X):
        X_scaled = self.scaler.transform(X[:, 1:])
        X_transformed =  np.dot(X_scaled, self.VT.T[:, :self.n_components])
        return np.c_[X[:, 0], X_transformed] # добавляем id обратно в массив
    
    def get_sigma(self):
        return self.Sigma
    
    def fit_transform(self, X):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X[:, 1:])

        U, Sigma, VT = np.linalg.svd(X_scaled, full_matrices=False)
        self.full_Sigma = Sigma.copy()

        for i in range(self.n_components, len(Sigma)): # выделение главных сингулярных чисел матрицы
            Sigma[i] = 0

        self.VT = VT
        self.Sigma = Sigma

        X_transformed =  np.dot(X_scaled, self.VT.T[:, :self.n_components])
        return np.c_[X[:, 0], X_transformed] # добавляем id обратно в массиви и возвращаем уже отредактированный массив np [id, features]
    
def remove_components(features, n_components):
    pca = PCA(n_components=n_components)
    features = pca.fit_transform(features)
    #print('Sigma values:', pca.get_sigma())
    print('Information rate: {:.2f}%'.format(pca.information_rate() * 100))
    return features  