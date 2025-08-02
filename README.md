# Global Healthcare Data ETL & Analysis CLI

A command-line Python project that extracts COVID-19 data from a public API, transforms it using pandas, and loads it into a MySQL database for analysis via CLI queries.

API(url)-https://coviddata.github.io/coviddata/v1/countries/stats.json

## Table of Contents

- Project Overview
- Features
- Tech Stack
- Project Structure
- Getting Started
- CLI Usage
- Database Schema
- Sample Queries

## Project Overview

This project simulates a real-world ETL pipeline:
- Extracts COVID-19 case data from a REST API.
- Transforms and cleans the data using pandas.
- Loads it into a structured MySQL table.
- Allows CLI-based querying for analytical insights.

## Features

- API data extraction based on country and date range
- Daily case tracking (new/total cases & deaths)
- Command-line querying for:
  - Total cases
  - Daily trends
  - Top N affected countries
- Logging and error handling
- Modular Python codebase

## Tech Stack

| Tool         | Purpose                          |
|--------------|----------------------------------|
| Python       | Core programming language        |
| pandas       | Data transformation              |
| MySQL        | Data storage and querying        |
| mysql-connector-python | Python ↔ MySQL bridge |
| argparse     | CLI Interface                    |
| logging      | ETL process monitoring           |


## Project Structure

revature_project/
│
├── main.py (CLI entry point)
├── api_client.py (API fetch logic)
├── data_transformer.py (Data cleaning & transformation)
├── mysql_handler.py (MySQL DB operations)
├── sql/
│ └── create_tables.sql (Table schema)
├── config.ini (DB credentials)
├── requirements.txt (Dependencies)
└── README.md (Project documentation)

## Getting Started

### 1. Clone the repo

git clone https://github.com/vinayak327/global-healthcare-etl-cli.git
cd global-healthcare-etl-cli

### 2. Set up virtual environment

python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

### 3. Configure your config.ini

[mysql]
host = localhost
user = root
password = yourpassword

database = healthcare_db

### 4. Run CLI

python main.py list_tables

### 5. CLI Usage

# Fetch and load data
python main.py fetch_data India 2020-03-01 2020-03-31

# Query total cases
python main.py query_data total_cases India

# View all tables
python main.py list_tables

# Drop tables (use with caution)
python main.py drop_tables

## Database Schema (daily_cases)

| Column Name   | Data Type   | Description                  |
|---------------|-------------|------------------------------|
| id            | INT, PK     | Auto-increment primary key   |
| report_date   | DATE        | Date of report               |
| country_name  | VARCHAR     | Name of the country          |
| total_cases   | BIGINT      | Cumulative cases till date   |
| new_cases     | INT         | Cases reported that day      |
| total_deaths  | BIGINT      | Cumulative deaths till date  |
| new_deaths    | INT         | Deaths reported that day     |
| etl_timestamp | TIMESTAMP   | Auto-recorded insert time    |


## Sample Queries

Here are some example commands you can run using the CLI:

# Fetch and store COVID-19 data for a specific country and date range
python main.py fetch_data India 2023-01-01 2023-01-31

# Get total confirmed COVID-19 cases for a country
python main.py query_data total_cases India

# Get total confirmed deaths for a country
python main.py query_data total_deaths India

# View daily trends (cases or deaths) for a specific country
python main.py query_data daily_trends India new_cases
python main.py query_data daily_trends India new_deaths

# View the top 5 most affected countries by total cases
python main.py query_data top_affected 5

# List all tables in the database
python main.py list_tables

# Drop all tables (use only if needed)
python main.py drop_tables





