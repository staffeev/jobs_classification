import pandas as pd
import numpy as np
import pickle
# import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering


if __name__ == "__main__":
    df = pickle.load(open('./datasets/data.pickle', 'rb'))
    n_resumes = df.shape[0]
    emb_len = len(df.iloc[0]['bag_of_words'])
    print(f'loaded {n_resumes} resumes')
    def distance(chel1, chel2):
        return cosine_distances([chel1['bag_of_words']], [chel2['bag_of_words']])[0, 0]
    coords = np.zeros((n_resumes, emb_len))
    for i, row in df.iterrows():
        coords[i] = row['bag_of_words'] * 10 + row['bag_of_words_desc']
    clustering = AgglomerativeClustering(n_clusters=50).fit(coords)
    labels = clustering.labels_
    df['cluster'] = pd.Series(labels)
    print('clustered')
    from sklearn.manifold import TSNE
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(coords)
    print('projected')
    #plt.ion()
    import plotly.express as px
    df['x'] = X_embedded[:, 0]
    df['y'] = X_embedded[:, 1]
    df.to_pickle("./datasets/clusters.pickle")
    fig = px.scatter(df, x="x", y="y", color="cluster", hover_data=['name', 'description'])
    fig.show()

