#!/usr/bin/env bash

# Postgres позволяет подключиться к удаленной базе указав ссылку на нее после флага -d
# ссылка подгрузится из переменной окружения, которую нам нужно будет указать на сервисе деплоя
# дальше мы загружаем в поключенную базу наш sql-файл с таблицами
#pip install --upgrade pip && pip install poetry && psql -a -d $DATABASE_URL -f database.sql
make install && psql -a -d $DATABASE_URL -f database.sql
