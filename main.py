from PCA_class import PCA
import features_correction

def main():
    pca = PCA(n_components=300)
    features = features_correction.get_correct_features()
    pca.fit(features)
    print('Sigma values:', pca.get_sigma())
    print('Information rate: {:.2f}%'.format(pca.information_rate() * 100))

if __name__ == "__main__":
    main()
