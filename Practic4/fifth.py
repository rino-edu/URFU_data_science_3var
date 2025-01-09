import csv
import sqlite3
import json

def connect_to_db(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE breweries (
            brewery_id INTEGER PRIMARY KEY,
            brewery_name TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE beers (
            beer_beerid INTEGER PRIMARY KEY,
            beer_name TEXT,
            beer_style TEXT,
            beer_abv REAL,
            brewery_id INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beer_beerid INTEGER NOT NULL,
            review_time INTEGER,
            review_profilename TEXT,
            review_overall REAL,
            review_aroma REAL,
            review_appearance REAL,
            review_palate REAL,
            review_taste REAL
        )
    """)

def insert_data(csv_filepath, json_filepath, db):
  cursor = db.cursor()

  with open(csv_filepath, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        
      cursor.execute("""
                      INSERT OR IGNORE INTO breweries 
                      (brewery_id, brewery_name) 
                      VALUES (?, ?)
                              """, (row['brewery_id'], row['brewery_name']))
      
      cursor.execute("""
                      INSERT OR IGNORE INTO beers 
                      (beer_beerid, beer_name, beer_style, beer_abv, brewery_id) 
                      VALUES (?, ?, ?, ?, ?)
                              """, (row['beer_beerid'], row['beer_name'], row['beer_style'], row['beer_abv'], row['brewery_id']))
      
      cursor.execute("""
                      INSERT INTO reviews 
                      (beer_beerid, review_time, review_profilename, review_overall, 
                      review_aroma, review_appearance, review_palate, review_taste) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                     """, 
                      (row['beer_beerid'], row['review_time'], row['review_profilename'], row['review_overall'], 
                      row['review_aroma'], row['review_appearance'], row['review_palate'], row['review_taste']))


  with open(json_filepath, "r", encoding="utf-8") as f:
    json_data = json.load(f)
    for item in json_data:
        cursor.execute("""
                       INSERT OR IGNORE INTO breweries 
                       (brewery_id, brewery_name) 
                       VALUES (?, ?)
                               """, (item['brewery_id'], item['brewery_name']))
        
        cursor.execute("""
                       INSERT OR IGNORE INTO beers 
                       (beer_beerid, beer_name, beer_style, beer_abv, brewery_id) 
                       VALUES (?, ?, ?, ?, ?)
                               """, (item['beer_beerid'], item['beer_name'], item['beer_style'], item['beer_abv'], item['brewery_id']))
        cursor.execute("""
                       INSERT INTO reviews 
                       (beer_beerid, review_time, review_profilename, review_overall, 
                       review_aroma, review_appearance, review_palate, review_taste) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                         (item['beer_beerid'], item['review_time'], item['review_profilename'], item['review_overall'], 
                          item['review_aroma'], item['review_appearance'], item['review_palate'], item['review_taste']))

  db.commit()

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
        b.brewery_id,
        b.brewery_name,
        r.review_time,
        r.review_overall,
        r.review_aroma,
        r.review_appearance,
        r.review_profilename,
        be.beer_style,
        r.review_palate,
        r.review_taste,
        be.beer_name,
        be.beer_abv,
        be.beer_beerid
        FROM reviews AS r
        JOIN beers AS be ON r.beer_beerid = be.beer_beerid
        JOIN breweries AS b ON be.brewery_id = b.brewery_id
        LIMIT 25;
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_1.json")

#2 Средняя оценка для каждого стиля пива
def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT beer_style, AVG(review_overall) AS average_rating
        FROM beers AS b
        JOIN reviews AS r ON b.beer_beerid = r.beer_beerid
        GROUP BY beer_style
        ORDER BY average_rating DESC;
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_2.json")

#3 Отзывы пользователя с наибольшим количеством отзывов
def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
        r.review_profilename, be.beer_name, be.beer_style, r.review_overall, r.review_aroma,
        r.review_appearance, r.review_palate, r.review_taste
        FROM reviews AS r
        JOIN beers AS be ON r.beer_beerid = be.beer_beerid
        WHERE r.review_profilename in (
                                        SELECT review_profilename
                                        FROM reviews
                                        GROUP BY review_profilename
                                        ORDER BY COUNT(*) DESC
                                        LIMIT 1
                                    )
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_3.json")

#4 Все позиции пшеничного пива с abv больше 4
def fourth_query(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT DISTINCT b.brewery_name, be.beer_name, be.beer_style, be.beer_abv
        FROM breweries AS b
        JOIN beers AS be ON b.brewery_id = be.brewery_id
        WHERE be.beer_style LIKE '%weizen%'
        AND be.beer_abv > 4
        AND be.beer_abv != "";
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_4.json")

#5 топ 3 самых вкуснопахнущих позиций
def fifth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT be.beer_name, AVG(r.review_aroma) AS average_aroma
        FROM beers AS be
        JOIN reviews AS r ON be.beer_beerid = r.beer_beerid
        GROUP BY be.beer_name
        ORDER BY average_aroma DESC
        LIMIT 3;
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_5.json")

#6 Пивоварни, имющие среднюю оценку своих позиций меньше 3.5
def sixth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT b.brewery_name, AVG(r.review_overall) AS avg_brewery_rating
        FROM breweries AS b
        JOIN beers AS be ON b.brewery_id = be.brewery_id
        JOIN reviews AS r ON be.beer_beerid = r.beer_beerid
        GROUP BY b.brewery_name
        HAVING AVG(r.review_overall) < 3.5;
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    save_results(items, "5_6.json")

db = connect_to_db("fifth.db")
#create_tables(db)

#insert_data("5/beer_reviews.csv", "5/breweries.json", db)

#first_query(db)
#second_query(db)
#third_query(db)
#fourth_query(db)
#fifth_query(db)
#sixth_query(db)