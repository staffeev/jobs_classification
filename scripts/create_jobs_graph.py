import sys
sys.append("../jobs_classification")
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import networkx as nx
from matplotlib import pyplot as plt


def f():
    df = pickle.load(open('datasets/clusters.pickle', 'rb'))
    dfs = df.sort_values(["resume_id", "start_date"])
    shifted = dfs.shift(1, fill_value=-1)
    dfs[["prev_cluster", "prev_name", "prev_coords"]] = shifted[["cluster", "name", "coords"]]
    
    dfs = dfs[dfs["resume_id"] == shifted["resume_id"]]
    dfs[["prev_cluster", "prev_name", "prev_coords", "cluster", "name", "coords"]].to_pickle("datasets/jobs_connections.pickle")


def draw_graph_from_df(df):
    graph = nx.from_pandas_edgelist(df)
    nx.draw(graph)
    plt.show()


def get_center_of_cluster(df, column_name):
    df2 = pd.DataFrame(df.to_dict())
    df2["avg_cluster_coords"] = df2.groupby(column_name)["coords"].transform("mean")
    df2["dif_coords"] = df2.apply(lambda x: cosine_distances([x["coords"]], [x["avg_cluster_coords"]])[0, 0], axis=1)
    df2["center_cluster_coord"] = df2.groupby(column_name)["dif_coords"].transform("min")
    group = df2.groupby(column_name)["dif_coords"].transform("idxmin")
    df2["cluster_name"] = df2.loc[group, "name"].values
    return df2.loc[group, "name"].values


if __name__ == "__main__":
    con = pickle.load(open('./datasets/jobs_connections.pickle', 'rb'))
    con["cluster_name"] = get_center_of_cluster(con, "cluster")
    con["prev_cluster_name"] = get_center_of_cluster(con, "prev_cluster")

    graph_info = con.groupby(["cluster", "cluster_name", "prev_cluster_name"]).size().reset_index()
    graph_info = graph_info.rename(columns={
        0: "weight", "cluster_name": "source", "prev_cluster_name": "target"
    })

    draw_graph_from_df(graph_info)


    