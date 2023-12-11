FROM python:latest

WORKDIR /src/

COPY ./src /src

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y mariadb-server mariadb-client

RUN service mariadb start && mariadb -u root -proot -e "CREATE DATABASE ploio_db;"
RUN service mariadb start && mariadb -u root -proot -e "CREATE USER 'root'@'%' IDENTIFIED BY 'root';"
RUN service mariadb start && mariadb -u root -proot -e "GRANT ALL PRIVILEGES ON ploio_db.* TO 'root'@'%';"
RUN service mariadb start && mariadb -u root -proot -e "FLUSH PRIVILEGES;"

ENV DATABASE_URL="mysql+pymysql://root:root@host.docker.internal:3306/ploio_db"

WORKDIR /src/

CMD uvicorn --host=0.0.0.0 --port 8000 main:app
