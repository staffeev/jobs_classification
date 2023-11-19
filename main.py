from scripts.parsing import parsing_pipe
from scripts.processing import processing_pipe
from scripts.clustering import clustering_pipe
from argparse import ArgumentParser
from settings import FIELDNAMES, PATH_TO_JOBS_DATASET, PATH_TO_RESUMES
from functions import get_cloud, show_cloud, get_frequencies
import asyncio
import pandas as pd

parser = ArgumentParser()
parser.add_argument("--dataset_path", default=PATH_TO_JOBS_DATASET, type=str,
                    help="Путь к датасету с занятостями")
parser.add_argument("--create_dataset", default=False, action="store_true", 
                    help="Флаг, нужно ли создавать датасет")
parser.add_argument("--save_pickles", default=False, action="store_true", 
                    help="Флаг, нужно ли сохранять pickle на каждом этапе")                 
parser.add_argument("--folder_path", default=PATH_TO_RESUMES, type=str,
                    help="Указание пути с файлами резюме")
parser.add_argument("-show_wordcloud", choices=FIELDNAMES, type=str)
parser.add_argument("-test", choices=["parsing", "processing", "clustering"], type=str)


async def main():
    args = parser.parse_args()
    if args.create_dataset:
        df = await parsing_pipe(args.folder_path, save_pickle=args.save_pickles)
    else:
        df = pd.read_csv(PATH_TO_JOBS_DATASET)
    df = await processing_pipe(df, save_pickle=args.save_pickles)
    clustering_pipe(df)
    if args.show_wordcloud:
        show_cloud(get_cloud(get_frequencies(args.show_wordcloud, args.dataset_path)))


if __name__ == "__main__":
    asyncio.run(main())