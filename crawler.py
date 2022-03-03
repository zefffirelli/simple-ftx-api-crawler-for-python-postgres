from datetime import datetime, timedelta
from dateutil import rrule
import psycopg2
from psycopg2 import errorcodes, errors
import requests

# Global Configuration
psql_connection_string = "dbname=postgres user=postgres password=postgres"
endpoint_url = 'https://ftx.com/api'
start_period = datetime(2022, 1, 3)
resolution = 60 #seconds
markets = ['BTC-PERP', 'ETH-PERP'] # Add as many markets as you want

# Crawler functions
def update_periods():
    '''
    Maintain a list of available periods and update table
    '''
    # Generate available periods
    for market in markets:
        for day in rrule.rrule(rrule.DAILY, dtstart=start_period, until=datetime.now()):
            # Skip if already in the database
            conn = psycopg2.connect(psql_connection_string)
            cur = conn.cursor()
            query = """SELECT idperiod, market
                        FROM period
                        WHERE idperiod = '{}' AND market = '{}'""".format(day, market)
            try:            
                cur.execute(query)
                val = cur.fetchone()
                if not val:
                    # Load new period
                    record = (day, market, 'available')
                    ins = """INSERT INTO period (idperiod, market, status) VALUES(%s, %s, %s)"""
                    try:
                        cur.execute(ins,record)
                        print('{}: {} Period was loaded'.format(day, market))
                        conn.commit()
                    except Exception as e:
                        print("Error :", e)
            except Exception as e:
                print("Error :", e)

def get_available_results():
    '''
    Get list of available results by future and period
    '''
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    query = """SELECT idperiod, market
                FROM period
                WHERE status = 'available' OR status = 'failed'"""
    try:
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            return None
        else:
            return results
    except Exception as e:
            print("Error :", e)
            return None

def get_result(period, market):
    '''
    Get a single result and return the data
    '''
    # Manage dates, datetime, and resolution range of results
    _resolution = str(resolution)
    start_date = period
    end_date = start_date + timedelta(minutes=1439)
    # Get the historical market data as JSON
    request_url = f'{endpoint_url}/markets/{market}'
    result = requests.get(f'{request_url}/candles?resolution={_resolution}&start_time={start_date.timestamp()}&end_time={end_date.timestamp()}').json()
    if result['success'] == True:
        data = (market, result)
        return data
    else:
        return None

def load_result(data):
    '''
    Load a single result and return the status
    '''
    market = data[0]
    result = data[1]
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    for index, row in enumerate(result['result']):
        # Convert record into tuple for postgres
        date = row['startTime']
        open = row['open']
        high = row['high']
        low = row['low']
        close = row['close']
        volume = row['volume']
        query = """INSERT INTO perps 
            (idperp, date, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        try:
            cur.execute(query, (market, date, open, high, low, close, volume))
        except Exception as e:
            print("Error :", e)
            conn.rollback()
            return 'failed'
    conn.commit()
    return 'loaded'

def crawl_results():
    '''
    Initiate crawler
    '''
    # Update available results
    print('Updating available results...')
    update_periods()
    # Get available results
    available_results = get_available_results()
    if available_results:
        # Crawl available results
        print('Crawling available results...')
        for index, row in enumerate(available_results):
            period = row[0]
            market = row[1]
            print('Crawling {} of {}: {} {}'.format(index +1, len(available_results), period, market))
            # Get and load result
            data = get_result(period, market)
            if not data:
                status = 'failed'
            else:
                status = load_result(data)
            # Update database status
            conn = psycopg2.connect(psql_connection_string)
            cur = conn.cursor()
            ins = """UPDATE period 
                    SET status = '{}' 
                    WHERE idperiod = '{}' AND market = '{}'""".format(status, period, market)
            try:
                cur.execute(ins)
                conn.commit()
            except Exception as e:
                print("Error :", e)
                conn.rollback()
    print('Crawl is complete')            

if __name__ == '__main__':
    crawl_results()

