FROM python:3.8.5

ENV PYTHONBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./app/
