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