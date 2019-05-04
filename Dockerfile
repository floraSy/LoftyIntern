FROM python:3.7.2-alpine3.9
LABEL MAINTAINER florayunshen@gmail.com

COPY . /Documents
CMD ["python3", "-u", "./main.py"]
