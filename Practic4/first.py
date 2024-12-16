import json
import sqlite3
import csv

def connect_to_db(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def load_csv(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if len(row) == 0: continue
            item = {
                'id': int(row[0]),
                'name': row[1],
                'street': row[2],
                'city': row[3],
                'zipcode': int(row[4]),
                'floors': int(row[5]),
                'year': int(row[6]),
                'parking': 1 if row[7] == "True" else 0,
                'prob_price': int(row[8]),
                'views': int(row[9])
            }
            items.append(item)

    return items

def create_buildings_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE buildings (
            id integer primary key,
            name text,
            street text,
            city text,
            zipcode integer,
            floors integer,
            year integer,
            parking integer,
            prob_price integer,
            views integer
        )
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO buildings (id, name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES (:id, :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)
    """, items)
    db.commit()

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM buildings
        ORDER BY year
        LIMIT 13
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            SUM(prob_price) as buildings_price_sum,
            MIN(year) as min_year,
            MAX(year) as max_year,
            ROUND(AVG(prob_price), 2) as avg_prob_price
        FROM buildings
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items[0]

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            city,
            COUNT(*) as count
        FROM buildings
        GROUP BY city
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM buildings
        WHERE year > 2000
        ORDER BY year
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 1
# create_buildings_table(connect_to_db("first.db"))
# 2
# items = load_csv("1-2/item.csv")
db = connect_to_db("first.db")
# insert_data(db, items)
# 3

# first = first_query(db)
# save_results(first, "1_1.json")

# second = second_query(db)
# save_results(second, "1_2.json")

# third = third_query(db)
# save_results(third, "1_3.json")

fourth = fourth_query(db)
save_results(fourth, "1_4.json")