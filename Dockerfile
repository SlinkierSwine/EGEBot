FROM python:3.8

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt