
class models():

    class Clusters: 

        def K_Means(self,n_clusters=8):
            from sklearn.cluster import KMeans
            return KMeans(n_clusters=int(n_clusters))

        def DB_SCAN(self,eps=0.5,min_samples=5 ):
            from sklearn.cluster import DBSCAN
            return DBSCAN(eps=float(eps),min_samples=int(min_samples))

