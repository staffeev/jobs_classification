FROM python:3.8.3-slim-buster
COPY . /src
RUN apt-get update
RUN apt-get install -y gcc g++ wget
RUN pip install -r /src/requirements.txt
RUN wget https://github.com/deeppavlov/DeepPavlov/blob/1.3.0/deeppavlov/configs/spelling_correction/levenshtein_corrector_ru.json -O /src/data/levenshtein.json
RUN wget https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar -O /src/data/navec.tar
# CMD ["/usr/bin/python", "-m", "jupyterlab", "--allow-root", "--no-browser", "--app-dir=/src"]
