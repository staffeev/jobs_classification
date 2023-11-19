import os
import sys
 
# setting path
sys.path.append('../jobs_classification')
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import locale
import re
import aiofiles
import asyncio
import pickle
from logger import make_logger
from settings import PATH_TO_PICKLE
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
PICKLE_PARSED = "parsed.pickle"
logger = make_logger(__name__)

EDU_TYPE_TO_VALUE = {
    'Неоконченное высшее образование': 2, 
    'Высшее образование (Магистр)': 4, 
    'Higher education': 3, 
    'Высшее образование (Бакалавр)': 3, 
    'Среднее специальное образование': 1, 
    'Образование': 0, 
    'Высшее образование (Кандидат наук)': 5, 
    'Среднее образование': 1, 
    'Высшее образование': 3
}
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", 
           "Октябрь", "Ноябрь", "Декабрь"]
FIELDNAMES = ["job_id", "resume_id", "start_date", "num_month", "name", "description", "sex", "birthday", "edu_level", "num_lang", "skills", "filename"]


class Resume:
    """Класс для резюме"""
    def __init__(self, id_: int, path: str, parent_list: list):
       self.id_ = id_
       self.path = path
       self.parent_list = parent_list
       self.content = None
       self.soup = None
    
    async def get_data(self):
        await self.open_file()
        self.parent_list.append(self.process())
    
    async def open_file(self):
        """Сохранение файла в переменную"""
        async with aiofiles.open(self.path, encoding="UTF-8") as file:
            self.content = await file.read()
            # self.content = self.content.replace(u"\xa0", u" ")
            self.soup = bs(self.content, "lxml")
    
    def process(self):
        """Обработка информации из html"""
        if self.soup is None:
            raise KeyError("There is no content in this resume")
        main_div = self.soup.find("div", {"class": "resume-applicant"})
        birth_info = main_div.find("div", {"class": "bloko-columns-row"})\
            .find("div", {"class": "resume-header-title"})
        edu_info =  main_div.find("div", {"data-qa": "resume-block-education"})
        language_info = main_div.find("div", {"data-qa": "resume-block-languages"})
        skills_info = main_div.find("div", {"data-qa": "skills-table"})
        experience_info = main_div.find("div", {"data-qa": "resume-block-experience"})
        return (
            self.id_,
            *self._process_birth_info(birth_info), self._process_education(edu_info),
            self._process_languages(language_info), self._process_skills(skills_info),
            self._process_experience(experience_info), self.path
        )
    
    def _process_birth_info(self, div):
        """Получение информации о рождении"""
        paragraph = div.find("p")
        sex = paragraph.find("span", {"data-qa": "resume-personal-gender"})
        if not sex is None:
            sex = sex.text
        birth_date = paragraph.find("span", {"data-qa": "resume-personal-birthday"})
        date = None
        if not birth_date is None:
            birth_date = birth_date.text
            date = datetime.now()
        return sex, date
    
    def _process_education(self, div):
        """Получение информации об образовании"""
        if div is None:
            return None
        type_of_edu = div.find("div", {"class": "bloko-columns-row"}).text
        return EDU_TYPE_TO_VALUE[type_of_edu]
    
    def _process_languages(self, div):
        """Получение информации о языках"""
        if div is None:
            return None
        langs = div.find("div", {"class": "bloko-tag-list"}).findAll("p")
        return len(langs)
    
    def _process_skills(self, div):
        """Получение инфорации о навыках"""
        if div is None:
            return None
        skills = div.find("div", {"class": "bloko-tag-list"})\
            .findAll("span", {"class": "bloko-tag__section"})
        return [i.text for i in skills]
    
    def _process_experience(self, div):
        """Получение информации о местах работы"""
        if div is None:
            return None
        jobs = div.find("div", {"class": "resume-block-item-gap"})\
            .findAll("div", {"class": "resume-block-item-gap"})
        return [self._process_job(job) for job in jobs]
    
    def _process_job(self, div):
        """Получение информации об одном месте работы"""
        duration, experience = div.findAll("div", {"class": "bloko-column"})
        duration_value = duration.find("div", {"class": "bloko-text"})

        number_of_months = re.search("\d+\sм", duration_value.text)
        number_of_years = re.search("\d+\s[\bг\b|\bл\b]", duration_value.text)
        value = 0
        if not number_of_months is None:
            value += int(re.search("\d+", number_of_months[0])[0])
        if not number_of_years is None:
            value += int(re.search("\d+", number_of_years[0])[0]) * 12

        start_date_text = duration.text.split()
        start_date = datetime(
            month=MONTHS.index(start_date_text[0])+1, year=int(start_date_text[1]), day=1)
        if "по настоящее время" in duration.text:
            value = (datetime.now() - start_date) // 2629746

        job_name = experience.find("div", {"data-qa": "resume-block-experience-position"})
        job_description = experience.find("div", {"data-qa": "resume-block-experience-description"})
        return start_date, value, job_name.text, job_description.text


def convert_resume_to_jobs(data):
    """Конвертация одного резюме в список занятостей"""
    id_, sex, birthday, edu_level, num_lang, skills, jobs, path = data
    if not skills is None: 
        skills = ", ".join(skills)
    result = []
    for job in jobs:
        start_date, num_months, name, descr = job
        result.append((id_, start_date, num_months, name, descr, sex, birthday, edu_level, num_lang, skills, path))
    return result


def convert_resumes_to_jobs(data):
    """Конвертация резюме в список занятостей"""
    job_counter = 1
    result = []
    for resume in data:
        for job in convert_resume_to_jobs(resume):
            result.append((job_counter, *job))
            job_counter += 1
    return result


def return_to_pipeline(data: list):
    """Сохранение данных из html в csv"""
    df = pd.DataFrame(data, columns=FIELDNAMES)
    return df


async def main(path, save_pickle=False):
    folder_path = path
    paths = os.listdir(folder_path)
    proccessed = []
    resumes_list = [Resume(ix, folder_path + p, proccessed) for ix, p in enumerate(paths, 1)]
    await asyncio.gather(*[r.get_data() for r in resumes_list])
    logger.info("resumes getted")
    converted = convert_resumes_to_jobs(proccessed)
    logger.info("resumes converted to jobs")
    df = return_to_pipeline(converted)
    if save_pickle:
        df.to_pickle(PATH_TO_PICKLE + PICKLE_PARSED)
        logger.info("parsed pickle file dumped")
    return df


async def parsing_pipe(path, save_pickle=False):
    logger.info("parsing started")
    return await main(path)


# if __name__ == "__main__":
#     asyncio.
#     path = "PATH_TO_RESUMES"
#     print(parsing_pipeline(path))