import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances, pairwise_distances, cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import networkx as nx
from matplotlib import pyplot as plt


def draw_graph_from_df(df, **kwargs):
    graph = nx.from_pandas_edgelist(df, **kwargs)
    graph.draw()
    plt.show()


if __name__ == "__main__":
    con = pickle.load(open('./datasets/jobs_connections.pickle', 'rb'))
    con["avg_cluster_coords"] = con.groupby("cluster")["coords"].transform("mean")
    con["dif_coords"] = con.apply(lambda x: cosine_distances([x["coords"]], [x["avg_cluster_coords"]])[0, 0], axis=1)
    con["center_cluster_coord"] = con.groupby("cluster")["dif_coords"].transform("min")
    group = con.groupby("cluster")["dif_coords"].transform("idxmin")
    con["cluster_name"] = con.loc[group, "name"].values

    con = con.join(
        con[["name", "cluster"]].rename(
            columns={"name": "prev_cluster_name", "cluster": "prev_cluster"}
        ), on="prev_cluster", rsuffix="_r"
    )
    print(con)


    # graph_info = con.groupby(["cluster", "cluster_name", "prev_cluster_name"]).size().reset_index()
    # print(graph_info)
    # draw_graph_from_df(graph_info, source="prev_cluter_name", target="claster_name", )


    