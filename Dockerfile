FROM python:3.5
LABEL MAINTAINER florayunshen@gmail.com

RUN pip install pandas
RUN pip install bs4
RUN pip install requests
RUN mkdir -p /home/LoftyCode/InternResults


COPY main.py /home/LoftyCode/InternResults/
WORKDIR /home/LoftyCode/InternResults


CMD ["python3", "-u", "./main.py"]