FROM python:3.10

WORKDIR /app

COPY .env /app
COPY requirements.txt /app
COPY ./src /app

RUN pip install -r requirements.txt

CMD python main.py