import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from settings import EDU_TYPE_TO_VALUE
import locale
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
        if self.soup is None:
            raise KeyError("There is no content in this resume")
        main_div = self.soup.find("div", {"class": "resume-applicant"})
        birth_info = main_div.find("div", {"class": "bloko-columns-row"})\
            .find("div", {"class": "resume-header-title"})
        edu_info =  main_div.find("div", {"data-qa": "resume-block-education"})
        language_info = main_div.find("div", {"data-qa": "resume-block-languages"})
        skills_info = main_div.find("div", {"data-qa": "skills-table"})
        # print(skills_info)
        return self._process_skills(skills_info)
    

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


    def save_to_csv(self):
        """Сохранение в csv"""
        pass


if __name__ == "__main__":
    stat = {}
    head = 20
    folder_path = "./data/resumes/"
    paths = os.listdir(folder_path)
    for p in paths:
        try:
            r = Resume(folder_path + p)
            r.open_file()
            res = tuple(r.process())
            # stat[len(res)] = stat.get(len(res), 0) + 1
            for i in res:
                stat[i] = stat.get(i, 0) + 1
        except:
            pass
    for i in sorted(stat, key=lambda x: stat[x], reverse=True)[:head]:
        print(i, stat[i])