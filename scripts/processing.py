import pymorphy2
import re
from navec import Navec
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

    morph = pymorphy2.MorphAnalyzer()
    TO_DELETE = {'CONJ', 'PREP', 'PRCL', 'INTJ', 'NUMR', 'NPRO'}


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
        lst_string = no_wspace_string.split()
        
        if lst_string == []:
            return "<pad>"
        
        spell_check_lst = []
        for word in lst_string:
            if word not in navec:
                for spell_checked_word in spell_check(word):
                    spell_check_lst.append(spell_checked_word)
            else:
                spell_check_lst.append(word)
        
        normal_form_lst = []
        for word in spell_check_lst:
            if word not in navec:
                morph_word = morph.parse(word)[0]
                if morph_word.tag.POS not in TO_DELETE:
                    normal_form = morph_word.normal_form.replace("ё", "е")
                    for sub in normal_form.split():
                        normal_form_lst.append(sub)
            else:
                normal_form_lst.append(word)

        root_search_lst = []
        for word in normal_form_lst:
            if word not in navec:
                for root_searched_word in root_search(word):
                    root_search_lst.append(root_searched_word)
            else:
                root_search_lst.append(word)

        if root_search_lst == []:
            return "<pad>"

        return " ".join(root_search_lst)

    def to_vec(string: str):
        return sum([navec[word] for word in string.split() if word in navec])
    
    df[NORMALIZED_NAME] = df[NAME].apply(normalize) 
    df[NORMALIZED_DESCRIPTION] = df[DESCRIPTION].apply(normalize) 
    logger.info("text fields normalized")
    df[NAME_VEC] = df[NORMALIZED_NAME].apply(to_vec)
    df[DESCRIPTION_VEC] = df[NORMALIZED_DESCRIPTION].apply(to_vec)
    logger.info("text fields vectorized")

    if save_pickle:
        df.to_pickle(PATH_TO_PICKLE + PICKLE_PROCESSED)
        logger.info("processed pickle file dumped")
    return df
