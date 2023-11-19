import sys
sys.path.append("../jobs_classification")
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import networkx as nx
from settings import RESUME_ID, START_DATE, CLUSTER_ID, CLUSTER_NAME, COORDS, \
    PREV_CLUSTER_NAME, PREV_CLUSTER_ID, PREV_COORDS, NAME, PREV_NAME
from matplotlib import pyplot as plt


def get_prev_cluster_info(df):
    """Для каждой занятости получает кластер, в которому принадлежала предыдущая занятость"""
    dfs = df.sort_values([RESUME_ID, START_DATE])
    shifted = dfs.shift(1)
    dfs[[PREV_NAME, PREV_CLUSTER_ID, PREV_CLUSTER_NAME, PREV_COORDS]] = shifted[[NAME, CLUSTER_ID, CLUSTER_NAME, COORDS]]
    dfs = dfs[dfs[RESUME_ID] == shifted[RESUME_ID]]
    dfs[[PREV_CLUSTER_ID, PREV_CLUSTER_NAME, PREV_COORDS, PREV_NAME,
         CLUSTER_ID, CLUSTER_NAME, COORDS, NAME]].to_pickle("datasets/jobs_connections.pickle")
    return dfs
    

def draw_graph_from_df(df):
    graph = nx.from_pandas_edgelist(df)
    nx.draw(graph)
    plt.show()


if __name__ == "__main__":
    con = pickle.load(open('./datasets/clusters.pickle', 'rb'))
    con = get_prev_cluster_info(con)
    graph_info = con.groupby([CLUSTER_ID, CLUSTER_NAME, PREV_CLUSTER_ID, PREV_CLUSTER_NAME]).size().reset_index()
    graph_info = graph_info.rename(columns={
        0: "weight", CLUSTER_NAME: "source", PREV_CLUSTER_NAME: "target"
    })

    draw_graph_from_df(graph_info)


    