import psycopg2
import datetime
import dblogger
import psycopg2.extras

def get_db_conn():
    DB_HOST = "34.116.206.104"
    DB_NAME = "style-and-tryon-app"
    DB_USER = "postgres"
    DB_PASSWORD = "M03d68d71!"

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
            db_log.write(str(datetime.datetime.now()) + str(e) + "\n")

def close_db_conn(conn, cur):
    try:
        conn.close()
        cur.close()
        dblogger.log("Close connection to PostgreSQL successfully!\n")
    except Exception as e:
        with open("db_log.txt", "a") as db_log:
            dblogger.log(str(e))

