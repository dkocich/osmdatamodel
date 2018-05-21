FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  libproj-dev \
  python-gdal \
  libxml2-dev \
  libxslt1-dev \
  python-dev
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD [ "python3", "code/manage.py runserver 0.0.0.0:8000" ]
