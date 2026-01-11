import os

import psycopg2
import dblogger
import psycopg2.extras
from dotenv import load_dotenv

def connect():
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    try:
        conn = psycopg2.connect(
            host = DB_HOST,
            database = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dblogger.log("Connected to PostgreSQL successfully!\n")

        return conn, cur

    except Exception as e:
        with open("db_log.txt", "a") as db_log:
            db_log.write(str(e))

def disconnect(conn, cur):
    try:
        conn.close()
        cur.close()
        dblogger.log("Close connection to PostgreSQL successfully!\n")
    except Exception as e:
        with open("db_log.txt", "a") as db_log:
            dblogger.log(str(e))

