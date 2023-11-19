# Программа кластеризации сельскохозяйственных профессий
Репозиторий разработки программы для [кластеризации](https://rshbdigital.ru/agrocode-hack/agrocode-hack2023-task3) сельскохозяйственных профессий на основе резюме.

##  Как обработать данные и посмотреть кластеры?

Программа поделена на две части:
1) обработка данных из html и создание кластеров;
2) визуализация данных;

Запуск программы обработки данных осуществляется запуском файла `main.py` командой `python main.py --create_dataset` для Windows (или `python3 main.py --create_dataset` для Linux), параметр обязателен. В результате работы будут созданы некотоые файлы, главный из которых - `datasets/clusters.pickle`.

Визуализация осуществляется запуском сервера, на котором грузится холст с кластерами. Команда для поднятия сервера - `uvicorn server.main:app`, выполняемая из основной папки с программой. Сервер грузит файл `datasets/cluster.pickle`, из данных которого рисует графы. Собственно при замене этого файла на другой с таким же именем будут визуализироваться кластеры из нового файла.
Адрес, при переходе на который будут отображаться кластеры - `http://127.0.0.1:8000`
