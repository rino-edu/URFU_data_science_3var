import json
from pymongo import MongoClient
import pandas as pd
import pymongo
import common

def connect_db():
    client = MongoClient()
    db = client['db-2024']
    return db.jobs

def read_csv(filepath):
    df = pd.read_csv(filepath, sep=';')
    data = df.to_dict('records')
    return data
  

collection = connect_db()
#collection.insert_many(read_csv("task_1_item.csv"))

def sort_by_salary(collection):
    return list(collection.find(limit=10).sort({"salary": pymongo.DESCENDING}))

# query1 = sort_by_salary(collection)
# common.save_in_json(query1, "5_1.json")

# query2 = list(collection.find({'age': {'$lt': 30}}).sort("salary": pymongo.DESCENDING).limit(15))
# common.save_in_json(query2, "5_2.json")

# query3 = list(collection.find(
#         { 
#             'city': 'Варшава',
#             'job': {'$in': ['Водитель', 'Учитель', 'Повар']}
#         }
#     ).sort('age', pymongo.ASCENDING).limit(10))

# common.save_in_json(query3, "5_3.json")

query4 = collection.count_documents(
    {
        'age': {'$gte': 18, '$lte': 35},
        'year': {'$gte': 2019, '$lte': 2022},
        '$or': [
            {'salary': {'$gt': 50000, '$lte': 75000}},
            {'salary': {'$gt': 125000, '$lt': 150000}},
        ],
    }
)

with open('5_4.json', 'w', encoding='utf-8') as f:
    json.dump(query4, f, ensure_ascii=False, indent=4)