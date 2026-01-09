import json
import os
import datetime

def upload_data(conn, cur):
    FOLDER_PATH = r"D:\ETTI\Anul_4\Proiect IA\Json_Script_Creator\json_files"
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".json")]
    total_inserted = 0

    for filename in files:
        file_path = os.path.join(FOLDER_PATH, filename)

        with open(file_path, 'r') as f:
            data = json.load(f)

            for item in data:
                item_id = item.get('id')
                brand = item.get('brand')
                category = item.get('category')
                gender = item.get('gender')
                url = item.get('url')
                colors = item.get('colors', [])
                style = item.get('style')

                price_raw = item.get('price_eur', '0')
                try:
                    price = float(price_raw)
                except ValueError:
                    price = 0.0

                try:
                    insert_query = """
                                   INSERT INTO clothes (id, brand, category, gender, url, colors, style, price_eur)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; \
                                   """

                    cur.execute(insert_query, (
                        item_id, brand, category, gender, url, colors, style, price
                    ))
                    total_inserted += 1

                except Exception as e:
                    with open("db.log.txt", "a") as db_log:
                        db_log.write(str(datetime.datetime.now()) + str(e) + "\n")
    conn.commit()
    with open("db.log.txt", "a") as db_log:
        db_log.write(f"Succefuly inserted {total_inserted} items!!! <3")
