FROM python:3-onbuild
LABEL MAINTAINER florayunshen@gmail.com

COPY . /usr/src/app
CMD ["python3", "-u", "main.py"]
