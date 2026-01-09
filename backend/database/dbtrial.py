import dbwrite
import dbread
import dbconn
import dblogger


if __name__ == "__main__":
    conn, cur = dbconn.get_db_conn()
    dblogger.log("Query DB trial run using gender = man and brand = zara")

    rez = dbread.query_db(cur)
    print(type(rez))

    dbread.query_to_json(rez)
    dblogger.log("Updated file.json")

    dbconn.close_db_conn(conn, cur)