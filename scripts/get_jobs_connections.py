import pandas as pd
import pickle
import sys
sys.path.append("../jobs_classification")



if __name__ == "__main__":
    df = pickle.load(open('datasets/clusters.pickle', 'rb'))
    df = df.rename(columns={"Unnamed: 0": "job_id", "id": "resume_id"})
    dfs = df.sort_values(["resume_id", "start_date"])
    shifted = dfs.shift(1, fill_value=-1)
    dfs[["prev_cluster", "prev_name", "prev_coords"]] = shifted[["cluster", "name", "coords"]]
    
    dfs = dfs[dfs["resume_id"] == shifted["resume_id"]]
    dfs[["prev_cluster", "prev_name", "prev_coords", "cluster", "name", "coords"]].to_pickle("datasets/jobs_connections.pickle")
