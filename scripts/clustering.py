import sys
sys.path.append("../jobs_classification")
import pandas as pd
import numpy as np
import pickle
from sklearn.manifold import TSNE
from settings import PATH_TO_JOBS_DATASET, JOB_VEC, \
    AVG_CLUSTEER_COORDS, \
    NAME, DESCRIPTION, COORDS_DIFFERENCE, \
    CENTER_CLUSTER_COORDS, CLUSTER_NAME, CLUSTER_ID
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering, HDBSCAN, KMeans


def get_center_of_cluster(df, column_name):
    """Получение имени из центральной точки кластера. column_name - столбец с координатами"""
    df2 = df.copy()
    df2[AVG_CLUSTEER_COORDS] = df2.groupby(column_name)[JOB_VEC].transform("mean")
    df2[COORDS_DIFFERENCE] = df2.apply(
        lambda x: cosine_distances([x[JOB_VEC]], [x[AVG_CLUSTEER_COORDS]])[0, 0], axis=1
    )
    df2[CENTER_CLUSTER_COORDS] = df2.groupby(column_name)[COORDS_DIFFERENCE].transform("min")
    group = df2.groupby(column_name)[COORDS_DIFFERENCE].transform("idxmin")
    df2[CLUSTER_NAME] = df2.loc[group, NAME].values
    return df2.loc[group, NAME].values


def clustering_pipeline(df):
    clustering = KMeans(n_clusters=50, random_state=0, n_init="auto").fit(np.stack(df[JOB_VEC]))
    labels = clustering.labels_
    df[CLUSTER_ID] = pd.Series(labels)
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)\
        .fit_transform(np.stack(df[JOB_VEC]))
    df[CLUSTER_NAME] = get_center_of_cluster(df, CLUSTER_ID)
    
    df['x'] = X_embedded[:, 0]
    df['y'] = X_embedded[:, 1]
    df.to_pickle("./datasets/clusters.pickle")

if __name__ == "__main__":
    df = pd.read_csv(PATH_TO_JOBS_DATASET)
    clustering_pipeline(df)
    
