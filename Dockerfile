FROM python:3-onbuild
LABEL MAINTAINER florayunshen@gmail.com

COPY . /Documents
CMD ["python3", "-u", "main.py"]
