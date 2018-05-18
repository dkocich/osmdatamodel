FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  libproj-dev \
  python-gdal
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
