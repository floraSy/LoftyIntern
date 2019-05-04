FROM python:3
LABEL MAINTAINER florayunshen@gmail.com

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
CMD ["python3", "-u", "./main.py"]
