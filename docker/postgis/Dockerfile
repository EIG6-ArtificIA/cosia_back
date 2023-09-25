FROM postgis/postgis:15-3.4
COPY ./init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
CMD ["docker-entrypoint.sh", "postgres"]