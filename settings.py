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
FIELDNAMES = ["id", "start_date", "num_month", "name", "description", "sex", "birthday", "edu_level", "num_lang", "skills", "filename"]
PATH_TO_NAVEC = "datasets/navec_hudlit_v1_12B_500K_300d_100q.tar"
PATH_TO_JOBS_DATASET = "datasets/jobs.csv"
PATH_TO_RESUMES = "data/resumes/"
NORMALIZED_NAME = "normalized_name"
NORMALIZED_DESCRIPTION = "normalized_description"
NAME_VEC = "name_vec"
DESCRIPTION_VEC = "description_vec"
NAME = "name"
DESCRIPTION = "description"
COORDS = "coords"
AVG_CLUSTEER_COORDS = "avg_cluster_coords"
COORDS_DIFFERENCE = "coords_dif"
CENTER_CLUSTER_COORDS = "center_cluster_coords"
CLUSTER_NAME = "cluster_name"
CLUSTER_ID = "cluster_id"
RESUME_ID = "resume_id"
START_DATE = "start_date"
PREV_SUFFIX = "prev_"
PREV_CLUSTER_ID = PREV_SUFFIX + CLUSTER_ID
PREV_CLUSTER_NAME = PREV_SUFFIX + CLUSTER_NAME
PREV_COORDS = PREV_SUFFIX + COORDS
PREV_NAME = PREV_SUFFIX + NAME