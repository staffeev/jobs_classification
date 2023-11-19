import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from itertools import chain
import pandas as pd
from settings import NAME, DESCRIPTION, NORMALIZED_NAME, CLUSTER_ID
import pickle

df = pickle.load(open('datasets/clusters.pickle', 'rb'))
clusters = {
    "name": list(df[NAME]),
    "normalized_name": list(df[NORMALIZED_NAME]),
    "description": list(df[DESCRIPTION]),
    "x": list(df["x"]),
    "y": list(df["y"]),
    "cluster": list(df[CLUSTER_ID])
}
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return open('server/index.html').read()

@app.get("/index.js", response_class=FileResponse)
def read_root():
    return 'server/index.js'

@app.get("/plotly.js", response_class=FileResponse)
def read_root():
    return 'server/plotly.js'

@app.get("/rainbow.js", response_class=FileResponse)
def read_root():
    return 'server/rainbow.js'

@app.get("/get_clusters")
def read_root():
    return clusters
