import sys
sys.path.append("../jobs_classification")
import pandas as pd
import numpy as np
import pickle
from sklearn.manifold import TSNE
from settings import PATH_TO_JOBS_DATASET, NAME_VEC, DESCRIPTION_VEC, COORDS, AVG_CLUSTEER_COORDS, \
    NAME, DESCRIPTION, COORDS_DIFFERENCE, CENTER_CLUSTER_COORDS, CLUSTER_NAME, CLUSTER_ID
import plotly.express as px
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering, HDBSCAN, KMeans



def distance(chel1, chel2):
    return cosine_distances([chel1['bag_of_words']], [chel2['bag_of_words']])[0, 0]


def get_center_of_cluster(df, column_name):
    """Получение имени из центральной точки кластера. column_name - столбец с координатами"""
    df2 = df.copy()
    df2[AVG_CLUSTEER_COORDS] = df2.groupby(column_name)[COORDS].transform("mean")
    df2[COORDS_DIFFERENCE] = df2.apply(
        lambda x: cosine_distances([x[COORDS]], [x[AVG_CLUSTEER_COORDS]])[0, 0], axis=1
    )
    df2[CENTER_CLUSTER_COORDS] = df2.groupby(column_name)[COORDS_DIFFERENCE].transform("min")
    group = df2.groupby(column_name)[COORDS_DIFFERENCE].transform("idxmin")
    df2[CLUSTER_NAME] = df2.loc[group, NAME].values
    return df2.loc[group, NAME].values


def clustering_pipeline(df):
    n_resumes = df.shape[0]
    # emb_len = len(df.iloc[0][NAME_VEC])
    print(f'loaded {n_resumes} resumes')
    def distance(chel1, chel2):
        return cosine_distances([chel1[NAME_VEC]], [chel2[NAME_VEC]])[0, 0]
    coords = np.zeros((n_resumes, emb_len))
    for i, row in df.iterrows():
        name_vec = np.zeros(emb_len) \
            if np.linalg.norm(row[NAME_VEC]) == 0 \
            else row[NAME_VEC] / np.linalg.norm(row[NAME_VEC])
        desc_vec = np.zeros(emb_len) \
            if np.linalg.norm(row[DESCRIPTION_VEC]) == 0 \
            else row[DESCRIPTION_VEC] / np.linalg.norm(row[DESCRIPTION_VEC])
        coords[i] = name_vec * 10 + desc_vec
        # coords[i] = name_vec
    clustering = KMeans(n_clusters=50, random_state=0, n_init="auto").fit(coords)
    labels = clustering.labels_
    df[CLUSTER_ID] = pd.Series(labels)
    print('clustered')
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)\
        .fit_transform(np.stack(df[COORDS]))   
    print('projected')
    df[CLUSTER_NAME] = get_center_of_cluster(df, CLUSTER_ID)
    
    df['x'] = X_embedded[:, 0]
    df['y'] = X_embedded[:, 1]
    df.to_pickle("./datasets/clusters.pickle")
    fig = px.scatter(df, x="x", y="y", color=CLUSTER_ID, hover_data=[NAME, DESCRIPTION])
    fig.show()

if __name__ == "__main__":
    df = pd.read_csv(PATH_TO_JOBS_DATASET)
    clustering_pipeline(df)
    
