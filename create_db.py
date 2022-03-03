import psycopg2
from crawler import psql_connection_string

def create_db():
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE postgres"
    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False
        cur.close()

def create_table(sql_query):
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()
        cur.close()

if __name__ == "__main__":
    # Create the desired database
    create_db()

    # Create the "period" table
    period_sql = """
        CREATE TABLE period (
            idperiod TIMESTAMP,
            market VARCHAR(20),
            status VARCHAR(20),
            PRIMARY KEY(idperiod, market)
        )
    """
    create_table(period_sql)

    # Create the "perps" table
    perps_sql = """
        CREATE TABLE perps (
            idperp VARCHAR(20),
            date TIMESTAMP,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume NUMERIC,
            PRIMARY KEY(idperp, date)
        )
    """
    create_table(perps_sql)