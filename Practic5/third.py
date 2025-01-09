import json
import pickle
import msgpack
from pymongo import MongoClient
import pandas as pd
import pymongo
import common

def connect_db():
    client = MongoClient()
    db = client['db-2024']
    return db.jobs

def read_pkl(file):
    with open(file, "rb") as f:
        return pickle.load(f)

collection = connect_db()
# collection.insert_many(read_pkl("task_3_item.pkl"))

# query1 = collection.delete_many(
#     {
#         "$or": [
#             {"salary": {"$lt": 25000}}, 
#             {"salary": {"$gt": 175000}}
#         ]
#     }
# )
# print(f"Удалено документов (запрос 1): {query1.deleted_count}")

# query2 = collection.update_many({}, {"$inc": {"age": 1}})
# print(f"Обновлено документов (запрос 2): {query2.modified_count}")

# query3 = collection.update_many(
#     {
#         "job": {"$in": ["Врач", "Учитель"]}
#     }, 
#     {
#         "$mul": {"salary": 1.05}
#     }
# )
# print(f"Обновлено документов (запрос 3): {query3.modified_count}")

# query4 = collection.update_many(
#     {
#         "city": {"$in": ["Прага", "Варшава"]}
#     }, 
#     {
#         "$mul": {"salary": 1.07}
#     }
# )
# print(f"Обновлено документов (запрос 3): {query4.modified_count}")

# query5 = collection.update_many(
#     {
#         "city": "Баку", 
#         "job": {"$in": ["Бухгалтер", "Менеджер"]}, 
#         "age": {"$gte": 50, "$lte": 70}
#     },
#     {
#         "$mul": {"salary": 1.10}
#     }
# )
# print(f"Обновлено документов (запрос 5): {query5.modified_count}")

query5 = collection.delete_many(
    {
        "city": "София", 
        "job": "Продавец", 
    },
)
print(f"Удалено документов (запрос 5): {query5.deleted_count}")