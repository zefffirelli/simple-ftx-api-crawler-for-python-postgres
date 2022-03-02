# Simple FTX API Crawler using Python and Postgres

## 0. Basic setup
- Install Postgres
- Create a new virtualenv: navigate to the desired folder location and run python3 -m venv YOUR_PROJECT_NAME
- Download this project into the above folder location
- Update the psql_connection_string in crawler.py to match your Postgres credentials

## 1. Run create_db.py to setup the database

## 2. Run crawler.py
- Global configuration variables allow you to adjust:
 - Time period: how many days are you crawling?
 - Resolution: what granularity of candle are you getting? Resolution is in seconds; 1 minute = 60,  1 day = 3600
 - Markets: which Perp markets are you crawling? Add any many as you wish.
