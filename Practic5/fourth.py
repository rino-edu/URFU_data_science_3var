import json
from pymongo import MongoClient
import pandas as pd
import pymongo
import common

def db_coonect():
  client = MongoClient()
  db = client['db-2024']
  return db.beer

def db_insert_data(collection, filepath_csv, filepath_json):
  try:
    df = pd.read_csv(filepath_csv, sep=',')
    data = df.to_dict('records')
    collection.insert_many(data)

    with open(filepath_json, 'r', encoding='utf-8') as f:
      data = json.load(f)
      collection.insert_many(data)

  except Exception as e:
    print(f"An unexpected error occurred: {e}")

def save_before_json(collection):
  before = list(collection.find().sort('id', 1))
  common.save_in_json(before, '4_before.json')

def querying(collection):
    # 1 задание
    #1 Все пива от Black Sheep и Amstel
    result = list(collection.find(
        {
        'brewery_name': {'$in': ['Black Sheep Brewery PLC', 'Amstel Brouwerij B. V.']}
        }
    ))
    common.save_in_json(result, '4_1_1.json')
    
    #2 Пиво с рейтингом больше 4.5
    result = list(collection.find({"review_overall": {"$gt": 4.5}}))
    common.save_in_json(result, '4_1_2.json')

    #3 Все пшенички с рейтингом ниже 4
    result = list(collection.find(
        {
            "beer_style": {"$regex": "weizen"},
            "review_overall": {"$lt": 4}
        }
    ))
    common.save_in_json(result, '4_1_3.json')

    #4 Позиции пива со вкусом больше 4.3 и хапаъом меньше 3.7
    result = list(collection.find(
        {
            "review_taste": {"$gt": 4.5}, 
            "review_aroma": {"$lt": 4.5}
        }
    ))
    common.save_in_json(result, '4_1_4.json')

    #5 первые 5 видов пива, оцененные больше чем на 4.85
    result = list(collection.find({"review_overall": {"$gt": 4.85}}).sort("review_time", 1).limit(5))
    common.save_in_json(result, '4_1_5.json')


    # Задание 2
    #1 Средний рейтинг пивоварен
    query = [
        {
            "$group": 
            {
                "_id": "$brewery_name", 
                "avg_rating": {"$avg": "$review_overall"}
            }
        }
    ]
    result = list(collection.aggregate(query))
    common.save_in_json(result, '4_2_1.json')


    #2 Количество пива для каждого сорта
    query = [
        {
            "$group": 
            {
                "_id": "$beer_style", 
                "count": {"$sum": 1}
            }
        }
    ]
    result = list(collection.aggregate(query))
    common.save_in_json(result, '4_2_2.json')

    #3  Минимум, Максимум и Средний review_palate для каждой пивоварни
    query = [
        {
            "$group":
            {
                "_id": "$brewery_name",
                "max_palate": {"$max": "$review_palate"},
                "min_palate": {"$min": "$review_palate"},
                "avg_palate": {"$avg": "$review_palate"},
            }
        },
        {
            "$sort":
            {
                "max_palate": -1,
            }
        } 
    ]
    result = list(collection.aggregate(query))
    common.save_in_json(result, '4_2_3.json')

    #4 Минимум, Максимум и Средний рейтинг для сорта пива
    query = [
        {
            "$group":
            {
                "_id": "$beer_style",
                "max_overall": {"$max": "$review_overall"},
                "min_overall": {"$min": "$review_overall"},
                "avg_overall": {"$avg": "$review_overall"},
            }
        },
        {
            "$sort":
            {
                "avg_overall": -1,
            }
        } 
    ]
    result = list(collection.aggregate(query))
    common.save_in_json(result, '4_2_4.json')

    #5 Топ 10 ревьюеров по количеству отзывов
    query = [
        {
            "$group": 
            {
                "_id": "$review_profilename", 
                "review_count": {"$sum": 1}
            }
        },
        {
            "$sort": 
            {
                "review_count": -1
            }
        },
        {"$limit": 10} 
    ]
    result = list(collection.aggregate(query))
    common.save_in_json(result, '4_2_5.json')


    # Задание 3
    #1 Увеличить рейтинг на 0.1 для всех American IPA
    query = {"beer_style": "American IPA"}
    update = {"$inc": {"review_overall": 0.1}}
    result = collection.update_many(query, update)
    print(f"Запрос 1: Обновлено {result.modified_count} документов.")

    #2 Удалить все пиво от пивоварни Black Sheep Brewery PLC
    query = {"brewery_name": "Black Sheep Brewery PLC"}
    result = collection.delete_many(query)
    print(f"Запрос 2: Удалено {result.deleted_count} документов.")

    #3 Установить рейтинг == 99999 для dвсех "Боков"
    query = {"beer_style": "Bock"}
    update = {"$set": {"review_overall": 99999}}
    result = collection.update_many(query, update)
    print(f"Запрос 3: Обновлено {result.modified_count} документов.")

    #4 Уменьшить review_palate на 3% для всех пива стиля "American Pale Ale (APA)",  от пивоварни "West Virginia Brewing Company" с оценкой не меньше 4.
    query = {"beer_style": "American Pale Ale (APA)", 
            "brewery_name": "West Virginia Brewing Company", 
            "review_overall": {"$gte": 4}}
    update = {"$mul": {"review_palate": 0.97}} 
    result = collection.update_many(query, update)
    print(f"Запрос 4: Обновлено {result.modified_count} документов.")

    #5 Удалить все записи, где имя ревьюера содержит "smurf"
    query = {"review_profilename": {"$regex": "smurf"}}
    result = collection.delete_many(query)
    print(f"Запрос 5: Удалено {result.deleted_count} документов.")

    after = list(collection.find().sort('id', 1))
    common.save_in_json(after, '4_after.json')



collection = db_coonect()
#db_insert_data(collection, 'beer_reviews.csv', 'breweries.json')
#save_before_json(collection)
querying(collection)