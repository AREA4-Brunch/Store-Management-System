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

RUN rm -rf ./migrations

# ENTRYPOINT [ "python", "manage.py", "store_management_db_init" ]
ENTRYPOINT [ "python", "manage.py", "store_management_db_drop_upgrade_populate" ]

# for production / preserving data, does same as: store_management_db_init
# store_management_db_upgrade_populate
