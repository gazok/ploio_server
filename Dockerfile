FROM python:latest

WORKDIR /src/

COPY ./src /src

RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 main:app