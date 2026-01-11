import dbconn
import queryfactory
from decimal import Decimal

def query(filters):
    conn, cur = dbconn.connect()
    full_query, parameters = queryfactory.create(filters)
    cur.execute(full_query, parameters)
    return cur.fetchall()