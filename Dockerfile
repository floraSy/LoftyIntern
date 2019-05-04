FROM python:3
LABEL MAINTAINER florayunshen@gmail.com

ADD main.py/
CMD ["python3", "-u", "main.py"]
