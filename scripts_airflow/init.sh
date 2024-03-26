#!/usr/bin/env bash


airflow connections add 'mysql_conn'  --conn-uri "mysql+mysqldb://root:root_admin@mysqldb:3306/sales"
echo "----------------------------------------------------------------------------------"

