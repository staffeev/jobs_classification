import pymorphy2
import re
from navec import Navec
import pandas as pd
from settings import NORMALIZED_NAME, \
    NORMALIZED_DESCRIPTION, \
    NAME, \
    DESCRIPTION, \
    PATH_TO_NAVEC


async def normalization_pipeline(df: pd.DataFrame):
    navec = Navec.load(PATH_TO_NAVEC)

    def spell_check(string):
        return string

    morph = pymorphy2.MorphAnalyzer()
    TO_DELETE = {'CONJ', 'PREP', 'PRCL', 'INTJ', 'NUMR', 'NPRO'}


    def normalize(string: str) -> str:
        lower_string = string.lower()
        lower_string = lower_string.replace('\t', ' ').replace('\n', ' ')
        lower_string = lower_string.replace("зам.", "заместитель ") \
            .replace("нач.", "начальник ") \
            .replace("рук.", "руководитель ") \
            .replace("ген.", "генеральный ") \
            .replace("ст.", "старший ")
        no_number_string = re.sub(r'\d+', '', lower_string)
        no_punc_string = re.sub(r'[^\w\s]', ' ', no_number_string)
        no_wspace_string = no_punc_string.strip()
        lst_string = no_wspace_string.split()
        if lst_string == []:
            return "<pad>"
        pav_lst = []
        for word in lst_string:
            if word not in navec:
                for e in spell_check(word).split():
                    pav_lst.append(e)
            else:
                pav_lst.append(word)

        normalized_lst = []
        for i in pav_lst:
            word = morph.parse(i)[0]
            if word.tag.POS not in TO_DELETE:
                word = word.normal_form
                for sub in word.split():
                    normalized_lst.append(sub.replace("ё", "е"))

        return " ".join(normalized_lst)

    df[NORMALIZED_NAME] = df[NAME].apply(normalize) 
    df[NORMALIZED_DESCRIPTION] = df[DESCRIPTION].apply(normalize) 
    df.to_pickle("./datasets/resumes_norm.pickle")
    return df
