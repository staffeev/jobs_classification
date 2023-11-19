import timeit
import pandas as pd


def show_cloud(wordcloud, label="Облако слов", show_flag=False):
    """Отрисовка облака"""
    plt.figure(figsize=(20, 20))
    plt.title(label, fontdict={"fontsize": 22})
    plt.axis("off")
    plt.imshow(wordcloud)
    if show_flag: 
        plt.show()
    

def get_cloud(text: dict[str, int]):
    """Получение облака"""
    cloud = WordCloud(
        width=1000, height=750, random_state=1, max_words=2500, background_color='black', margin=10, colormap='Pastel2'
    ).generate_from_frequencies(text)
    return cloud


def get_frequencies(column, path):
    """Получение частотного словаря для столбца датасета"""
    df = pd.read_csv(path)
    return df.groupby(column).size().to_dict()
