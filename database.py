
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(DATABASE_URL)

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Connected successfully!")
        print(result.fetchone()[0])

def read_data(query):
    return pd.read_sql_query(query, engine)

if __name__ == "__main__":
    test_connection()
