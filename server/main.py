from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from itertools import chain
import pandas as pd
import pickle

df = pickle.load(open('../datasets/clusters.pickle', 'rb'))
clusters = {
    "name": list(df["name"]),
    "description": list(df["description"]),
    "x": list(df["x"]),
    "y": list(df["y"]),
    "cluster": list(df["cluster"])
}
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return open('index.html').read()

@app.get("/index.js", response_class=FileResponse)
def read_root():
    return 'index.js'

@app.get("/plotly.js", response_class=FileResponse)
def read_root():
    return 'plotly.js'

@app.get("/get_clusters")
def read_root():
    return clusters
