import json
import sqlite3

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def connect_to_db(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def create_reviews_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE reviews (
            id integer primary key,
            building_name text references buildings(name),
            rating real,
            convenience integer,
            security integer,
            functionality integer,
            comment text
        )
    """)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        items = json.load(file)
    return items

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO reviews (building_name, rating, convenience, security, functionality, comment)
        VALUES (:name, :rating, :convenience, :security, :functionality, :comment)
    """, items)
    db.commit()

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM reviews
        WHERE building_name = 'Страусятник 94'
        ORDER BY rating
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT b.id, b.name, r.rating, r.comment
        FROM buildings b
        JOIN reviews r ON b.name = r.building_name
        WHERE r.rating > 4.5
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT b.name, avg(r.rating) as avg_rating, avg(r.convenience) as avg_convenience, avg(r.security) as avg_security, avg(r.functionality) as avg_functionality
        FROM buildings b
        JOIN reviews r ON b.name = r.building_name
        GROUP BY b.name
        ORDER BY avg_rating DESC
        LIMIT 5
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

# 1
# create_reviews_table(connect_to_db("first.db"))

# 2
# items = load_json("1-2/subitem.json")
db = connect_to_db("first.db")
# insert_data(db, items)

# 3
# first = first_query(db)
# save_results(first, "2_1.json")

# second = second_query(db)
# save_results(second, "2_2.json")

third = third_query(db)
save_results(third, "2_3.json")