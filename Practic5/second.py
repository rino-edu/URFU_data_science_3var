import json
import msgpack
from pymongo import MongoClient
import pandas as pd
import pymongo
import common

def connect_db():
    client = MongoClient()
    db = client['db-2024']
    return db.jobs

def read_msgpack(file):
    with open(file, "rb") as f:
        return msgpack.load(f)

collection = connect_db()
# collection.insert_many(read_msgpack("task_2_item.msgpack"))

# 1
# query1 = [
#     {
#         "$group":{
#             "_id": None,
#             "max_salary": {"$max": "$salary"},
#             "min_salary": {"$min": "$salary"},
#             "avg_salary": {"$avg": "$salary"},
#         }
#     }     
# ]
# result1 = list(collection.aggregate(query1))
# common.save_in_json(result1, "2_1.json")

# 2
# query2 = [
#     {
#         "$group": {
#             "_id": "$job",
#             "count": {"$sum": 1},
#         }
#     }     
# ]
# result2 = list(collection.aggregate(query2))
# common.save_in_json(result2, "2_2.json")

# 3
# query3 = [
#     {
#         "$group":{
#             "_id": "$city",
#             "max_salary": {"$max": "$salary"},
#             "min_salary": {"$min": "$salary"},
#             "avg_salary": {"$avg": "$salary"},
#         }
#     }     
# ]
# result3 = list(collection.aggregate(query3))
# common.save_in_json(result3, "2_3.json")

# 4
# query4 = [
#     {
#     "$group":{
#         "_id": "$job",
#         "max_salary": {"$max": "$salary"},
#         "min_salary": {"$min": "$salary"},
#         "avg_salary": {"$avg": "$salary"},
#     }
#     }     
# ]
# result4 = list(collection.aggregate(query4))
# common.save_in_json(result4, "2_4.json")

# 5
# query5 = [
#     {
#         "$group":{
#             "_id": "$city",
#             "max_age": {"$max": "$age"},
#             "min_age": {"$min": "$age"},
#             "avg_age": {"$avg": "$age"},
#         }
#     }     
# ]
# result5 = list(collection.aggregate(query5))
# common.save_in_json(result5, "2_5.json")

# 6
# query6 = [
#     {
#         "$group":{
#             "_id": "$job",
#             "max_age": {"$max": "$age"},
#             "min_age": {"$min": "$age"},
#             "avg_age": {"$avg": "$age"},
#         }
#     }     
# ]
# result6 = list(collection.aggregate(query6))
# common.save_in_json(result6, "2_6.json")

# 7-8
# query7 = list(collection.find(limit=1).sort({'age':1, 'salary': -1}))
# common.save_in_json(query7, "2_7.json")

# query8 = list(collection.find(limit=1).sort({'age':-1, 'salary': 1}))
# common.save_in_json(query8, "2_8.json")

# 9
# query9 = [
#     {
#         "$match":{
#             "salary": {"$gt": 50000}
#         }  
#     },
#     {
#         "$group":{
#             "_id": "$city",
#             "max_age": {"$max": "$age"},
#             "min_age": {"$min": "$age"},
#             "avg_age": {"$avg": "$age"},
#         }
#     },
#     {
#         "$sort":{
#             "avg_age": -1,
#         }
#     }    
# ]
# result9 = list(collection.aggregate(query9))
# common.save_in_json(result9, "2_9.json")

# 10
# query10 = [
#     {
#         "$match":{
#             'city': 'Варшава',
#             'job': 'Повар',
#             '$or': [
#                 {'age': {'$gt': 18, '$lt': 25}},
#                 {'age': {'$gt': 50, '$lt': 60}},
#             ]
#         }  
#     },
#     {
#         "$group":{
#             "_id": "$city",
#             "max_salary": {"$max": "$salary"},
#             "min_salary": {"$min": "$salary"},
#             "avg_salary": {"$avg": "$salary"},
#         }
#     }, 
# ]
# result10 = list(collection.aggregate(query10))
# common.save_in_json(result10, "2_10.json")

# 11
query11 = [
    {
        "$match":{
            'city': {'$in': ['Прага', 'Баку']},
            'job': {'$in': ['Программист', 'IT-специалист']},
            'age': {'$gte': 22},
        }  
    },
    {
        "$group":{
            "_id": "$job",
            "max_salary": {"$max": "$salary"},
        }
    },
    {
        "$sort":{
            "max_salary": -1,
        }
    } 
]
result11 = list(collection.aggregate(query11))
common.save_in_json(result11, "2_11.json")