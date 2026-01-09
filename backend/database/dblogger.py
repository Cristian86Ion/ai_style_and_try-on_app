import datetime

def log(text):
    date_time = str(datetime.datetime.now())
    with open("db_log.txt", "a") as f:
        f.write(date_time + "> " + text + "\n")