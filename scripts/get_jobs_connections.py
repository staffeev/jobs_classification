import pandas as pd
import pickle


if __name__ == "__main__":
    df = pickle.load(open('../datasets/clusters.pickle', 'rb'))
    df = df.rename(columns={"Unnamed: 0": "job_id", "id": "resume_id"})
    dfs = df.sort_values(["resume_id", "start_date"])
    dfs["prev_cluster"] = dfs.shift(1, fill_value=-1)["cluster"]
    dfs = dfs[dfs["resume_id"] == dfs.shift(1)["resume_id"]]
    dfs[["prev_cluster", "cluster"]].to_csv("../datasets/jobs_connections.csv", index=False)
