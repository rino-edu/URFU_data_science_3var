import sqlite3
import json
import msgpack

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def connect_to_db(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def create_product_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE product (
            id integer primary key,
            name text,
            price float,
            quantity integer,
            category text,
            fromCity text,
            isAvailable integer,
            views integer,
            version INTEGER DEFAULT 0
        )
    """)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        items = []
        for item in json.load(file):
            if item.get('category') is not None:
                items.append(item)
    return items

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
    """, items)
    db.commit()

def read_msgpack(file):
    with open(file, "rb") as f:
        return msgpack.load(f)

def handle_updates(db, updates):

  cursor = db.cursor()

  for item in updates:
      if (item['method'] == 'remove'):
        cursor.execute("DELETE FROM product WHERE name = ?", (item['name'],))

      elif (item['method'] == 'price_percent'):
        cursor.execute('''
                      UPDATE product
                      SET price = ROUND(price * (1 + ?), 2),
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))
        

      elif (item['method'] == 'price_abs'):
        cursor.execute('''
                      UPDATE product
                      SET price = price + ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))

      elif (item['method'] == 'quantity_sub' or item['method'] == 'quantity_add'):
        cursor.execute('''
                      UPDATE product
                      SET quantity = quantity + ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))

      elif (item['method'] == 'available'):
        cursor.execute('''
                      UPDATE product
                      SET isAvailable = ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))
      db.commit()

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT name, version 
        FROM product 
        ORDER BY version DESC 
        LIMIT 10
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category, 
            SUM(price) AS sum_price, 
            MIN(price) AS min_price, 
            MAX(price) AS max_price, 
            AVG(price) AS avg_price,
            COUNT(*) AS num_products
        FROM product
        GROUP BY category
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category, 
            SUM(quantity) AS total_quantity, 
            MIN(quantity) AS min_quantity, 
            MAX(quantity) AS max_quantity, 
            AVG(quantity) AS avg_quantity,
            COUNT(*) AS num_products
        FROM product
        GROUP BY category
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT name, price, fromCity 
        FROM product 
        WHERE price > 50 AND isAvailable = 1 AND category = 'fruit'
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

db = connect_to_db("fourth.db")
#create_product_table(db)

#items = load_json("4/_product_data.json")
#insert_data(db, items)

#updates = read_msgpack("4/_update_data.msgpack")
#handle_updates(db, updates)

#first = first_query(db)
#save_results(first, "4_1.json")

#second = second_query(db)
#save_results(second, "4_2.json")

#third = third_query(db)
#save_results(third, "4_3.json")

fourth = fourth_query(db)
save_results(fourth, "4_4.json")