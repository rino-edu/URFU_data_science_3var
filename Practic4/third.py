import json
import pickle
import sqlite3

def connect_to_db(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def create_songs_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE songs (
            id integer primary key,
            artist text,
            song text,
            duration_ms integer,
            year integer,
            tempo real,
            genre text
        )
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre)
        VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre)
    """, items)
    db.commit()

def read_pickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def read_text(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    items = []
    item = {}
    for line in lines:
        if line == "=====\n":
            items.append(item)
            item = {}
            continue
        pair = line.strip().split("::")
        key = pair[0]
        if key in ["instrumentalness", "explicit", "loudness"]:
            continue
        if key in ["duration_ms", "year"]:
            pair[1] = int(pair[1])
        if key in ["tempo"]:
            pair[1] = float(pair[1])
        item[key] = pair[1]
    return items

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
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
            SUM(duration_ms) as duration_ms_sum,
            MIN(duration_ms) as min_duration_ms,
            MAX(duration_ms) as max_duration_ms,
            ROUND(AVG(duration_ms), 2) as avg_duration_ms
        FROM songs
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT genre, COUNT(*) AS count_genre
        FROM songs
        GROUP BY genre
        ORDER BY count_genre DESC
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        WHERE duration_ms > 300000
        ORDER BY year DESC
        LIMIT 18
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

#print(read_pickle("3/_part_1.pkl")[0].keys())

#print(read_text("3/_part_2.text")[0])

#['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre']

db = connect_to_db("third.db")
#create_songs_table(db)
#items = read_text("3/_part_2.text")
#items = read_pickle("3/_part_1.pkl")
#insert_data(db, items)

#first = first_query(db)
#save_results(first, "3_1.json")

#second = second_query(db)
#save_results(second, "3_2.json")

#third = third_query(db)
#save_results(third, "3_3.json")

fourth = fourth_query(db)
save_results(fourth, "3_4.json")