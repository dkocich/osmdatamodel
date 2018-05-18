
FROM django

ADD . /osmdatamodel

WORKDIR /osmdatamodel

RUN pip3 install -r requirements.txt

CMD [ "python3", "manage.py runserver 0.0.0.0:8000" ]

