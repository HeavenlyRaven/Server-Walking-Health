# Server-Walking-Health
Application backend

## Описание, согласно критериям:

1. Наличие согласованного [ТЗ](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/REST%20API%20%D0%92%D0%B5%D0%B1%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F.docx)
2. [ТЗ, оформленное в XML, корректное относительно DTD](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/Spec.xml)
3. ER диаграмма модели предметной области:

![Diagram](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/Diagram.png)
4. Скрипты для развёртывания системы: можно запустить [app.py](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/src/app.py) в режиме Development сервера, предварительно запустив [setup_db.py](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/setup_db.py) для создания базы данных, либо сбилдить с помощью [Докерфайла](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/Dockerfile) и запустить в контейнере (инструкция приведена ниже)\
5. Тестовые данные: [тестовые HTTP запросы](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/test.http)\
6. [Документация к API](https://github.com/HeavenlyRaven/Server-Walking-Health/blob/ID_version/API_documentation.md)\
7. Транзакций (помимо автоматически созданных самой СУБД) нет

## Deployment instruction:

1. Install **Docker**.
2. Pull the image from Docker Hub with `docker pull heavenlyraven/walking-health`
3. Then run your container using `docker run -p [-e IP=<I>] [-e NUMBER_OF_WORKERS=<N>] 80:8080 heavenlyraven/walking-health` optionally passing the number of workers <N> (2 by default)
and the IP-address of the host (0.0.0.0 by default)
