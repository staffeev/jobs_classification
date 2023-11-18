from simple_parsing import create_dataset
from argparse import ArgumentParser
from settings import FIELDNAMES
from functions import get_cloud, show_cloud, get_frequencies

parser = ArgumentParser()
parser.add_argument("--dataset_path", default="datasets/jobs.csv", type=str,
                    help="Путь к датасету с занятостями")
parser.add_argument("--create_dataset", default=False, action="store_true", 
                    help="Флаг, нужно ли создавать датасет")
parser.add_argument("--folder_path", default="data/resumes/", type=str,
                    help="Указание пути с файлами резюме")
parser.add_argument("--show_wordcloud", choices=FIELDNAMES, type=str)


if __name__ == "__main__":

    args = parser.parse_args()
    if args.create_dataset:
        create_dataset(args.folder_path)
    if args.show_wordcloud:
        show_cloud(get_cloud(get_frequencies(args.show_wordcloud, args.dataset_path)))