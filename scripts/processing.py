import re
import pandas as pd
import pickle
from logger import make_logger
from settings import NORMALIZED_NAME, \
    NORMALIZED_DESCRIPTION, \
    NAME_VEC, \
    DESCRIPTION_VEC, \
    NAME, \
    DESCRIPTION, \
    PATH_TO_NAVEC, \
    PATH_TO_PICKLE
from scripts.parsing import PICKLE_PARSED
from sentence_transformers import SentenceTransformer

PICKLE_PROCESSED = "processed.pickle"
logger = make_logger(__name__)


async def processing_pipe(df: pd.DataFrame, test_mode=False, save_pickle=False):
    logger.info("processing started")
    if test_mode:
        with open(PATH_TO_PICKLE + PICKLE_PARSED, 'wb') as f:
            df = pickle.load(f)
        logger.info("pickle file loaded")
    navec = Navec.load(PATH_TO_NAVEC)

    def spell_check(string):
        return [string]

    def root_search(string):
        return [string]

    TO_DELETE = {'CONJ', 'PREP', 'PRCL', 'INTJ', 'NUMR', 'NPRO'}
    model = SentenceTransformer('cointegrated/rubert-tiny2')

    def normalize(string: str) -> str:
        lower_string = string.lower()
        lower_string = lower_string.replace('\t', ' ').replace('\n', ' ').replace("ё", "е")
        lower_string = lower_string.replace("зам.", "заместитель ")\
            .replace("нач.", "начальник ")\
            .replace("рук.", "руководитель ")\
                .replace("ген.", "генеральный ")\
                    .replace("ст.", "старший ")
        no_number_string = re.sub(r'\d+','',lower_string)
        no_punc_string = re.sub(r'[^\w\s]',' ', no_number_string)
        no_wspace_string = no_punc_string.strip()
        return no_wspace_string

    def to_vec(string: str):
        return model.encode([string])[0]
    
    df[NORMALIZED_NAME] = df[NAME].apply(normalize) 
    df[NORMALIZED_DESCRIPTION] = df[DESCRIPTION].apply(normalize) 
    logger.info("text fields normalized")
    df[NAME_VEC] = df[NORMALIZED_NAME].apply(to_vec)
    # df[DESCRIPTION_VEC] = df[NORMALIZED_DESCRIPTION].apply(to_vec)
    logger.info("text fields vectorized")

    if save_pickle:
        df.to_pickle(PATH_TO_PICKLE + PICKLE_PROCESSED)
        logger.info("processed pickle file dumped")
    return df


if __name__ == "__main__":
    df = pickle.load()
