import os
import psycopg2
from dotenv import load_dotenv
from . import dblogger

load_dotenv()

def connect():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=5432,
            connect_timeout=5
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("DB CONNECT ERROR:", e)   # 👈 SHOW IT
        dblogger.log(e)
        raise

def disconnect(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

