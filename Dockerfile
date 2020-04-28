FROM python:3.7
MAINTAINER Özgür Amaç

ADD src /code
WORKDIR /code
RUN pip install -r requirements.txt

