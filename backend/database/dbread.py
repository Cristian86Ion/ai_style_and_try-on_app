from . import dbconn
from . import queryfactory

def query(filters):
    conn, cur = dbconn.connect()
    full_query, parameters = queryfactory.create(filters)
    cur.execute(full_query, parameters)
    results = cur.fetchall()
    dbconn.disconnect(conn, cur)
    return results