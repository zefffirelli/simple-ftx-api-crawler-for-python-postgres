README

0. Basic setup
- Install Postgres
- Create a new virtualenv: navigate the desired folder and run python3 -m venv YOUR_PROJECT_NAME
- Download this project and move files into the above folder
- Update the psql_connection_string in crawler.py to match your Postgres credentials

1. Run create_db.py to setup the database

2. Run crawler.py
- Global configuration variables allow you to adjust:
    -- Time period: how many days are you crawling?
    -- Resolution: what granularity of candle are you getting? Resolution is in seconds so 1 minute is 60 and 1 day is 3600
    -- Markets: which Perp markets are you crawling? Add any many as you wish.
