from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from itertools import chain
import pandas as pd
import pickle

df = pickle.load(open('../datasets/clusters.pickle', 'rb'))
clusters = df[['name', 'description', 'x', 'y', 'cluster']].values.tolist()
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return open('index.html').read()

@app.get("/index.js", response_class=FileResponse)
def read_root():
    return open('index.js').read()

@app.get("/get_clusters")
def read_root():
    return clusters
