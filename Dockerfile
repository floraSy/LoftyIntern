FROM python:3
LABEL MAINTAINER florayunshen@gmail.com

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
CMD ["python3", "-u", "./main.py"]
