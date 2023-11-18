from simple_parsing import create_dataset
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--create_dataset", default=False, action="store_true", 
                    help="Флаг, нужно ли создавать датасет")
parser.add_argument("--folder_path", default="data/resumes/", type=str,
                    help="Указание пути с файлами резюме")



if __name__ == "__main__":
    args = parser.parse_args()
    if args.create_dataset:
        create_dataset(args.folder_path)