import pandas as pd
import numpy as np
import pickle
from settings import PATH_TO_JOBS_DATASET, JOB_VEC, NORMALIZED_NAME, \
        NORMALIZED_DESCRIPTION, PATH_TO_NAVEC
from navec import Navec


def vectorize_pipeline(df):
    navec = Navec.load(PATH_TO_NAVEC)
    n_resumes = df.shape[0]
    emb_len = len(navec['сон'])
    coords = [np.zeros(emb_len)] * n_resumes

    def bag_of_words(string: str):
        return sum([navec[word] for word in string.split() if word in navec])

    for i, row in df.iterrows():
        name_vec = bag_of_words(row[NORMALIZED_NAME])
        desc_vec = bag_of_words(row[NORMALIZED_DESCRIPTION])

        name_vec = np.zeros(emb_len) \
            if np.linalg.norm(name_vec) == 0 \
            else name_vec / np.linalg.norm(name_vec)

        desc_vec = np.zeros(emb_len) \
            if np.linalg.norm(desc_vec) == 0 \
            else desc_vec / np.linalg.norm(desc_vec)

        coords[i] = name_vec * 10 + desc_vec

    df[JOB_VEC] = coords
    return df

if __name__ == "__main__":
    df = pd.read_csv(PATH_TO_JOBS_DATASET)
    vectorize_pipeline(df)
    
