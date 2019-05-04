FROM python:3
LABEL MAINTAINER florayunshen@gmail.com

COPY ./
CMD ["python3", "-u", "main.py"]
