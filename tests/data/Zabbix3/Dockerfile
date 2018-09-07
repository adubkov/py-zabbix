FROM  mysql:5
LABEL maintainer="Maksim Syomochkin <maksim77ster@gmail.com>"
ENV MYSQL_ROOT_PASSWORD=root_pwd \
  MYSQL_DATABASE=zabbix \
  MYSQL_USER=zabbix \
  MYSQL_PASSWORD=zabbix
COPY zabbix.sql /docker-entrypoint-initdb.d/zabbix.sql
EXPOSE 3306
