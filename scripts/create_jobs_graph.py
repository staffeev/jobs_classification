import sys
sys.path.append("../jobs_classification")
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import networkx as nx
from settings import RESUME_ID, START_DATE, CLUSTER_ID, CLUSTER_NAME, JOB_VEC, \
    PREV_CLUSTER_NAME, PREV_CLUSTER_ID, PREV_COORDS, NAME, PREV_NAME
from matplotlib import pyplot as plt
from gexfpy import stringify
from gexfpy import Gexf, Graph, Nodes, Edges, Node, Edge, Color


def get_prev_cluster_info(df):
    """Для каждой занятости получает кластер, в которому принадлежала предыдущая занятость"""
    dfs = df.sort_values([RESUME_ID, START_DATE])
    shifted = dfs.shift(1)
    dfs[[PREV_NAME, PREV_CLUSTER_ID, PREV_CLUSTER_NAME, PREV_COORDS]] = shifted[[NAME, CLUSTER_ID, CLUSTER_NAME, JOB_VEC]]
    dfs = dfs[dfs[RESUME_ID] == shifted[RESUME_ID]]
    dfs[[PREV_CLUSTER_ID, PREV_CLUSTER_NAME, PREV_COORDS, PREV_NAME,
         CLUSTER_ID, CLUSTER_NAME, JOB_VEC, NAME]].to_pickle("datasets/jobs_connections.pickle")
    return dfs


def create_graph(g):
    gexf = Gexf()
    gexf.graph = Graph()
    nodes = []
    edges = []
    c = 1
    for i in g:
        id1, name1 = i["cluster_id"] + 1, i["source"]
        id2, name2 = i["prev_cluster_id"] + 1, i["target"]
        n1 = Node(id=id1, label=name1, color=[Color(r=255, g=0, b=0)])
        n2 = Node(id=id2, label=name2, color=[Color(r=255, g=0, b=0)])
        if n1 not in nodes:
            nodes.append(n1)
        if n2 not in nodes:
            nodes.append(n1)
        edge = Edge(source=id2, target=id1, label=i["weight"])
        if edge not in edges:
            edges.append(edge)
    
    gexf.graph.nodes = [Nodes(node=nodes, count=len(nodes))]
    gexf.graph.edges = [Edges(edge=edges, count=len(edges))]
    s = stringify(gexf)
    return s
    

if __name__ == "__main__":
    con = pickle.load(open('./datasets/clusters.pickle', 'rb'))
    con = get_prev_cluster_info(con)
    graph_info = con.groupby([CLUSTER_ID, CLUSTER_NAME, PREV_CLUSTER_ID, PREV_CLUSTER_NAME]).size().reset_index()
    graph_info = graph_info.rename(columns={
        0: "weight", CLUSTER_NAME: "target", PREV_CLUSTER_NAME: "source"
    })
    # print(graph_info.to_dict())
    g = [i[1] for i in graph_info.iterrows()]
    with open("./datasets/graph.xml", "w", encoding="utf-8") as file:
        file.write(create_graph(g))
    # print(g[0])
    # create_graph(g)
    # create_graph(graph_info.to_dict())
    # draw_graph_from_df(graph_info)
    # graph_info.to_csv("./datasets/jobs_graph.csv")


    