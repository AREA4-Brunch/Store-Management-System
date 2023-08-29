FROM python:3-alpine

RUN mkdir -p /usr/service
WORKDIR /usr/service


# install dependencies
COPY ./libs ./libs
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

RUN echo 'Forcing image update from here #1'

# run the app
COPY ./manage.py ./manage.py
COPY ./app ./app

RUN rm -rf ./migrations

# ENTRYPOINT [ "python", "manage.py", "user_management_db_init" ]
ENTRYPOINT [ "python", "manage.py", "user_management_db_drop_upgrade_populate" ]
