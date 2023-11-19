import sys
sys.path.append("../jobs_classification")
import pandas as pd
import numpy as np
import pickle
from settings import PATH_TO_JOBS_DATASET, JOB_VEC, NORMALIZED_NAME, \
        NORMALIZED_DESCRIPTION, PATH_TO_NAVEC, VEC_LEN
from navec import Navec
from sklearn.metrics.pairwise import cosine_similarity
from scipy.special import softmax
from settings import WORD_TO_GET_WEIGHT
import pickle

# np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)       


def vectorize_pipeline(df):
    navec = Navec.load(PATH_TO_NAVEC)
    n_resumes = df.shape[0]
    emb_len = len(navec['сон'])
    coords = [np.zeros(emb_len)] * n_resumes


    def calc_score(word_a, words_b):
        result = [cosine_similarity([navec[word_a]], [navec.get(word_b, np.zeros(300))])[0, 0] \
                  for word_b in words_b]
        # if len(result) != len(words_b):
        #     print(words_b)
        return result
    

    def calc_scores(words_b):
        # print(words_b)
        res = [calc_score(word, words_b) for word in WORD_TO_GET_WEIGHT]
        # if len(res) == 0:
            # print(words_b)
        return softmax(np.array(res).mean(axis=0))
    
    # def bag_of_words(string: str):
    #     return sum([navec[word] for word in string.split() if word in navec])
    

    def bag_of_words(string: str):
        if not string:
            return np.zeros(300)
        words = string.split()
        scores = calc_scores(words)
        nvc = [navec.get(word, np.zeros(VEC_LEN)) for word in words]
        res = np.array([nvc[x] * scores[x] for x in range(len(words))])
        sum_ = res.sum(axis=0)
        if len(sum_) == 1:
            sum_ = sum_[0]
        return sum_

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
    df.to_pickle("./datasets/resumes_vec.pickle")
    return df


if __name__ == "__main__":
    # print(float("nan"))
    df = pickle.load(open('./datasets/resumes_norm.pickle', 'rb'))
    vectorize_pipeline(df)
    # df = pd.read_csv("./datasets/resumes_norm.csv")
    # vectorize_pipeline(df)
