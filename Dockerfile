FROM python:3.7.2-alpine3.9
LABEL MAINTAINER florayunshen@gmail.com

RUN mkdir -p /home/LoftyCode/InternResults
WORKDIR /home/LoftyCode/InternResults

COPY main.py /home/LoftyCode/InternResults/
RUN pip install --no-cache-dir -r main.py

COPY . /home/LoftyCode/InternResults
CMD ["python3", "-u", "./main.py"]