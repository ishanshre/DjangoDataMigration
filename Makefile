#!make

include .env

postgresDBContainer:
	docker run --name ${db_container_name} -e POSTGRES_USER=${db_username} -e POSTGRES_PASSWORD=${db_password} -e POSTGRES_DBNAME=${db_dbname} -p 5432:5432 -d postgres:latest