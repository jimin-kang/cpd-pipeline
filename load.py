from prefect import task
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv
import os

# required to fetch Postgres credentials from .env
load_dotenv()

def create_postgres_table():
    '''
    Create the cpd_incidents table in Postgres DB (cpd_db) if it doesn't exist.
    '''
    # establish connection to DB
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="cpd_db",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    # create cursor object to execute SQL
    cur = conn.cursor()
    
    # execute query
    # TODO: store query somewhere else
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS cpd_incidents (
            date_time TIMESTAMP,
            id INTEGER PRIMARY KEY,
            type TEXT,
            subtype TEXT,
            location TEXT,
            description TEXT,
            last_updated TIMESTAMP,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            hour INTEGER, 
            minute INTEGER,
            second INTEGER
        )
    '''
    cur.execute(create_table_query)

    # commit changes
    conn.commit()

    # close cursor and connection
    cur.close()
    conn.close()

@task
def load_into_postgres(df):
    '''
    Load the transformed data into the Postgres DB.
    '''
    # create table to insert data into as necessary
    create_postgres_table()

    # create Engine object to connect to DB
    engine = create_engine(f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5433/cpd_db")
        
    # insert data into Postgres DB into the 'cpd_incidents' table
    df.to_sql('cpd_incidents', engine, if_exists='replace')