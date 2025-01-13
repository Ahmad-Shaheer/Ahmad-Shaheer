FROM apache/superset:latest
COPY init_superset.sh /app/init_superset.sh
USER root
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --upgrade gevent
RUN pip install pillow
RUN pip install psycopg2-binary
USER superset
ENTRYPOINT ["/app/init_superset.sh"]
