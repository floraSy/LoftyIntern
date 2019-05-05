FROM python:3
LABEL MAINTAINER florayunshen@gmail.com


ADD https://github.com/floraSy/LoftyIntern/blob/master/main.py /home/LoftyCode/InternResults/
WORKDIR /home/LoftyCode/InternResults/
CMD ["python3", "-u", "main.py"]
