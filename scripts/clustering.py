import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from settings import PATH_TO_JOBS_DATASET, NAME_VEC, DESCRIPTION_VEC
import plotly.express as px
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering


def clustering_pipe(df):
    n_resumes = df.shape[0]
    emb_len = len(df.iloc[0][NAME_VEC])
    print(f'loaded {n_resumes} resumes')
    def distance(chel1, chel2):
        return cosine_distances([chel1[NAME_VEC]], [chel2[NAME_VEC]])[0, 0]
    coords = np.zeros((n_resumes, emb_len))
    for i, row in df.iterrows():
        coords[i] = row[NAME_VEC] * 10 + row[DESCRIPTION_VEC]
    clustering = AgglomerativeClustering(n_clusters=50).fit(coords)
    labels = clustering.labels_
    df['cluster'] = pd.Series(labels)
    print('clustered')
    
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(coords)
    print('projected')
    #plt.ion()
    
    df['x'] = X_embedded[:, 0]
    df['y'] = X_embedded[:, 1]
    df.to_pickle("./datasets/clusters.pickle")
    fig = px.scatter(df, x="x", y="y", color="cluster", hover_data=['name', 'description'])
    fig.show()


if __name__ == "__main__":
    df = pd.read_csv(PATH_TO_JOBS_DATASET)
    clustering_pipe(df)
    