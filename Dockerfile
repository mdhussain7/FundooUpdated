FROM python:latest
MAINTAINER mdhussain <mdhussainsabhussain@gmail.com>
RUN mkdir /fundoo
WORKDIR /fundoo
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get install -y --no-install-recommends python3-dev libmcrypt-dev default-mysql-client
RUN apt-get update && apt-get install -y apt-utils && apt-get install -y curl
RUN apt-get install redis-server -y
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
COPY . ./
CMD ["python","manage.py","runserver", "0.0.0.0:8000"]


