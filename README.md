# Simple FTX API Crawler using Python and Postgres

This crawler will obtain historical Perpetual Futures data from the FTX API for user configurable time periods and resolutions (e.g. 30 seconds, 1 minute, 5 minute etc.)

## 0. Basic setup
- Install Postgres
- Create a new virtualenv: navigate to the desired folder location and run python3 -m venv YOUR_PROJECT_NAME
- Download this project into the above folder location
- Update the psql_connection_string in crawler.py to match your Postgres credentials

## 1. Run create_db.py to setup the database
You will need to have a working Postgres instance and ensure that they user is specified in the configuration and they have the necessary permissions to create databases/tables.

Script will create the database and tables necessary to store the Period/Perps to crawl and the resulting data.

There are two tables: 

1) Period table stores the Period+Perp combinations and their statuses (available for crawling, loaded, or failed)

<img width="532" alt="Period Table" src="https://user-images.githubusercontent.com/100279323/156532934-7da86f71-88d9-4d6f-a6d8-e7089d8acb6e.png">

2) Perps table stores the Period+Perp combinations and their data (Open High Low Close Volume).The below table is storing data at a 1 minute resolution.
 
<img width="835" alt="Perps Table" src="https://user-images.githubusercontent.com/100279323/156532946-8ff97e31-cd6f-40a8-8733-5156740ea570.png">

## 2. Run crawler.py
Script will determine the available/uncrawled periods for the specified Perps and will run a crawler, getting the data at the specified resolution.

<img width="421" alt="Crawler in action" src="https://user-images.githubusercontent.com/100279323/156554447-11c32fc6-f1a3-4846-b257-b48f194b87c2.png">
<img width="421" alt="Crawler in action" src="https://user-images.githubusercontent.com/100279323/156536452-e968535c-75d7-43d8-9f5a-8b52be4c93a4.png">

- Global configuration variables allow you to adjust:
  - Time period: how many days are you crawling?
  - Resolution: what granularity of candle are you getting? Resolution is in seconds; 1 minute = 60,  1 day = 86400
  - Markets: which Perp markets are you crawling? Add any many as you wish.

