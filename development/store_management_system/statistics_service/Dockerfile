FROM bde2020/spark-python-template:3.3.0-hadoop3.3
# Image does COPY . /app and pip install -r ./requirements.txt on its own


WORKDIR /app

RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install -r /app/requirements_.txt

ENV PATH_MYSQL_CONNECTOR_JAR=/app/libs/mysql-connector-j-8.0.33.jar

CMD [ "python3.7", "/app/manage.py", "run", "--host=0.0.0.0", "--port=5000", "--debug" ]
