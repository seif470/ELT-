# Custom ELT Project

This repository contains a custom Extract, Load, Transform (ELT) project that utilizes Docker, Airflow, dbt, and PostgreSQL to demonstrate a simple ELT process.

## Repository Structure

1. **docker-compose.yaml**: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines multiple services:
   - `source_postgres`: The source PostgreSQL database running on port 5433.
   - `destination_postgres`: The destination PostgreSQL database running on port 5434.
   - `postgres`: The postgres database used to store metadata from Airflow.
   - `webserver`: The Web UI for Airflow.
   - `scheduler`: Airflow's scheduler to orchestrate your tasks.

2. **airflow**: This folder contains the Airflow project including the dags to orchestrate both elt script and dbt to complete the ELT workflow

3. **custom_postgres**: This folder contains the dbt project including all of the custom models we will be writing into the destination database

4. **source_db_init/init.sql**: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

## How It Works

1. **Docker Compose**: Using the `docker-compose.yaml` file, a couple Docker containers are spun up:
   - A source PostgreSQL database with sample data.
   - A destination PostgreSQL database.
   - A Postgres database to store Airflow metadata
   - The webserver to access Airflow throught the UI
   - Airflow's Scheduler

2. **ELT Process**: Within Airflow, you can Orchestrates the ELT process and manages task distribution, It runs the elt script first which load the data from source to destination then it runs dbt models that makes some transformation to destination database. 

3. **Database Initialization**: The `init.sql` script initializes the source database with sample data. It creates several tables and populates them with sample data.

## Getting Started

1. Ensure you have Docker and Docker Compose installed on your machine.
2. Clone this repository.
3. run docker compose up -d`.
4. Once all containers are up and running, you can access the Airflow UI at `http://localhost:8080`
5. Once that is all setup, you can head into Airflow, run the DAG and watch as the ELT process is orchestrated for you!
