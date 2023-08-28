FROM python:3-alpine

RUN mkdir -p /usr/service
WORKDIR /usr/service


# install dependencies
COPY ./libs ./libs
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt


# run the app
COPY ./manage.py ./manage.py
COPY ./app ./app

ENTRYPOINT [ "python", "manage.py", "user_management_db_init" ]
