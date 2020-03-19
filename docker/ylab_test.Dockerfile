FROM python:3.8.1-slim
RUN mkdir /project
WORKDIR /project
COPY requirements.txt /project/
COPY . /project/
RUN apt-get update \
    && apt-get install -y build-essential python-dev \
    && pip install -r requirements.txt \
    && apt-get purge -y build-essential python-dev \
    && apt-get autoremove -y \
    && apt-get clean