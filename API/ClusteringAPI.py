from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans

__author__ =  'Rohan Agrawal'

class ClusteringAPI:
    """
    ClusteringAPI class contains all of the functions
    required to get vector space representation required
    for k means, getting an appropriate value of k
    and performing k means algorithm
    """
    def initVectorizer(self, stopwords, N):
        """Initialize the sklearn tf idf vectorizer, set to ignore stopwords, N documents, 
        documents with higher document frequency than 0.8*N are ignored, 
        n grams of maximum length 3 are also considered"""
        return TfidfVectorizer(min_df = 1, max_df=N*8/10, max_features=N*10, ngram_range = (1,3), stop_words = stopwords)

    def getVectorSpace(self, v, dataset):   
        """
        takes a dataset consisting of sentences seperated by a sentenceseperator variable, 
        v is the vectorizer initialized through initVectorizer()
        returns vector space represenation of the dataset
        """
        return v.fit_transform(dataset)    
        
    def getK(self, X, penalty):
        """
        returns a value of K for the dataset X, that minimizes
        the cost function for Clustering
        cost function = Inertia value for clustering + k*penalty
        """
        km = KMeans( n_clusters = 1, init='k-means++', n_init=1, verbose = 0)
        km.fit(X)
        scores = [km.inertia_ + penalty]
        for true_k in range(2,10):
            km = KMeans( n_clusters = true_k, init='k-means++', n_init=75, verbose = 0)
            km.fit(X)
            scores.append(km.inertia_ + penalty * true_k)
            if scores[len(scores)-1] > scores[len(scores)-2]:
                break

        return scores.index(min(scores)) + 1
        
    def getClusterLabelsCenters(self, X, true_k):
        """
        performs k means clustering on the dataset X,
        and returns labels for each row of the dataset,
        and cluster centers.
        """
        km = KMeans( n_clusters = true_k, init='k-means++', n_init=75, verbose = 0)
        km.fit(X)
        return km.labels_, km.cluster_centers_