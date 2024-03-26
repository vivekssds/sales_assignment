#!/usr/bin/env bash


airflow connections add 'mysql_conn'  --conn-uri "mysql+mysqldb://root:root_admin@mysqldb:3306/sales"
echo "----------------------------------------------------------------------------------"

airflow variables add 'WEATHER_API_KEY'  '35bc2c1eac5372747f3f87683237b713'"