from scripts.parsing import parsing_pipeline
from scripts.normalize import normalization_pipeline
from scripts.clustering import clustering_pipeline
from argparse import ArgumentParser
from settings import FIELDNAMES, PATH_TO_JOBS_DATASET, PATH_TO_RESUMES
from functions import get_cloud, show_cloud, get_frequencies

parser = ArgumentParser()
parser.add_argument("--dataset_path", default=PATH_TO_JOBS_DATASET, type=str,
                    help="Путь к датасету с занятостями")
parser.add_argument("--create_dataset", default=False, action="store_true", 
                    help="Флаг, нужно ли создавать датасет")
parser.add_argument("--folder_path", default=PATH_TO_RESUMES, type=str,
                    help="Указание пути с файлами резюме")
parser.add_argument("--show_wordcloud", choices=FIELDNAMES, type=str)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.create_dataset:
        df = parsing_pipeline(args.folder_path)
        df = normalization_pipeline(df)
        clustering_pipeline(df)
    if args.show_wordcloud:
        show_cloud(get_cloud(get_frequencies(args.show_wordcloud, args.dataset_path)))