import sys
sys.path.append("../jobs_classification")
import pandas as pd
import numpy as np
import pickle
from sklearn.manifold import TSNE
from settings import PATH_TO_JOBS_DATASET, NAME_VEC, DESCRIPTION_VEC, COORDS, AVG_CLUSTEER_COORDS, \
    NAME, DESCRIPTION, COORDS_DIFFERENCE, CENTER_CLUSTER_COORDS, CLUSTER_NAME, CLUSTER_ID, PATH_TO_PICKLE
import plotly.express as px
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering
from logger import make_logger
from processing import PICKLE_PROCESSED


PICKLE_CLUSTERED = "clustered.pickle"
logger = make_logger(__name__)


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


def clustering_pipe(df, test_mode=False, save_pickle=False):
    if test_mode:
        with open(PATH_TO_PICKLE + PICKLE_PROCESSED, 'wb') as f:
            df = pickle.load(f)
        logger.info("pickle file loaded")
    n_jobs = df.shape[0]
    # emb_len = len(df.iloc[0][NAME_VEC])
    logger.info(f'loaded {n_jobs} jobs for clusterization')
    df[COORDS] = df[NAME_VEC] * 10 + df[DESCRIPTION_VEC] 
    clustering = AgglomerativeClustering(n_clusters=50).fit(np.stack(df[COORDS]))
    labels = clustering.labels_
    df[CLUSTER_ID] = pd.Series(labels)
    logger.info('jobs clustered')
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)\
        .fit_transform(np.stack(df[COORDS]))   
    logger.info('clusters projected')
    df[CLUSTER_NAME] = get_center_of_cluster(df, CLUSTER_ID)
    
    df['x'] = X_embedded[:, 0]
    df['y'] = X_embedded[:, 1]
    if save_pickle:
        df.to_pickle(PATH_TO_PICKLE + PICKLE_CLUSTERED)
    # fig = px.scatter(df, x="x", y="y", color=CLUSTER_ID, hover_data=[NAME, DESCRIPTION])
    # fig.show()
    return df


if __name__ == "__main__":
    df = pd.read_csv(PATH_TO_JOBS_DATASET)
    clustering_pipe(df)
    