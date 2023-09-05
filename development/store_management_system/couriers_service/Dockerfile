FROM python:3.10-alpine

RUN mkdir -p /usr/service
WORKDIR /usr/service

# enable running python manage.py without specifying
# manage.py location
ENV PYTHONPATH .

# install dependencies
COPY ./libs ./libs
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

# run the app
COPY ./manage.py ./manage.py
COPY ./app ./app


ENV COMPILED_SOLIDTY_SRC_DIR_PATH=./libs/compiled_solidity


ENTRYPOINT [ "python", "manage.py", "run", "--host=0.0.0.0", "--port=5000", "--debug" ]
