import datetime

def log(text):
    date_time = str(datetime.datetime.now())
    with open("db.log.txt", "a") as f:
        f.write(f"{date_time}> {str(text)}\n")
