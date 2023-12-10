FROM python:latest

WORKDIR /src/

COPY ./src /src

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y mysql-server

RUN echo "mysql-server mysql-server/root_password password your_root_password" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password your_root_password" | debconf-set-selections

RUN service mysql start && mysql -u root -proot -e "CREATE DATABASE ploio_db;"
RUN service mysql start && mysql -u root -proot -e "CREATE USER 'root'@'%' IDENTIFIED BY 'root';"
RUN service mysql start && mysql -u root -proot -e "GRANT ALL PRIVILEGES ON ploio_db.* TO 'root'@'%';"
RUN service mysql start && mysql -u root -proot -e "FLUSH PRIVILEGES;"

ENV MYSQL_HOST=localhost
ENV MYSQL_PORT=3306
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root
ENV MYSQL_DATABASE=ploio_db

WORKDIR /src/

CMD uvicorn --host=0.0.0.0 --port 8000 main:app
