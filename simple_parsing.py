import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from settings import EDU_TYPE_TO_VALUE, MONTHS
import locale
import re
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class Resume:
    """Класс для резюме"""
    def __init__(self, path: str):
       self.path = path
       self.content = None
       self.soup = None
    
    def open_file(self):
        """Сохранение файла в переменную"""
        with open(self.path) as file:
            self.content = file.read()
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
        # print(skills_info)
        return self._process_experience(experience_info)
    
    def _process_birth_info(self, div):
        """Получение информации о рождении"""
        paragraph = div.find("p")
        sex = paragraph.find("span", {"data-qa": "resume-personal-gender"}).text
        birth_date = paragraph.find("span", {"data-qa": "resume-personal-birthday"}).text
        date = datetime.strptime(birth_date, "%d %B %Y")
        return sex, date
    
    def _process_education(self, div):
        """Получение информации об образовании"""
        type_of_edu = div.find("div", {"class": "bloko-columns-row"}).text
        return EDU_TYPE_TO_VALUE[type_of_edu]
    
    def _process_languages(self, div):
        """Получение информации о языках"""
        langs = div.find("div", {"class": "bloko-tag-list"}).findAll("p")
        return len(langs)
    
    def _process_skills(self, div):
        """Получение инфорации о навыках"""
        skills = div.find("div", {"class": "bloko-tag-list"})\
            .findAll("span", {"class": "bloko-tag__section"})
        return [i.text for i in skills]
    
    def _process_experience(self, div):
        """Получение информации о местах работы"""
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
            value = (datetime.now() - start_date).month

        job_name = experience.find("div", {"data-qa": "resume-block-experience-position"})
        job_description = experience.find("div", {"data-qa": "resume-block-experience-description"})
        return start_date, value, job_name.text, job_description.text


    def save_to_csv(self):
        """Сохранение в csv"""
        pass


if __name__ == "__main__":
    stat = {}
    head = 20
    count = 0
    folder_path = "./data/resumes/"
    paths = os.listdir(folder_path)
    for p in paths:
        r = Resume(folder_path + p)
        r.open_file()
        res = tuple(r.process())
        stat[res] = stat.get(res, 0) + 1
        # stat[len(res)] = stat.get(len(res), 0) + 1
        # for i in res:
        #     stat[i] = stat.get(i, 0) + 1
        break
    print("Количество", count)
    for i in sorted(stat, key=lambda x: stat[x], reverse=True)[:head]:
        print(i, stat[i])