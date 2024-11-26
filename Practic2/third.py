import json
import msgpack
import os
from collections import defaultdict

input_file = 'third_task.json'
result_json = 'result_3.json'
result_msgpack = 'result_3.msgpack'

try:
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()


aggregated_data = defaultdict(lambda: {"prices": []})

for item in data:
    name = item["name"]
    price = item["price"]
    aggregated_data[name]["prices"].append(price)

result = {}
for name, info in aggregated_data.items():
    prices = info["prices"]
    result[name] = {
        "average_price": sum(prices) / len(prices),
        "max_price": max(prices),
        "min_price": min(prices),
    }

with open(result_json, 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

with open(result_msgpack, 'wb') as file:
    msgpack.dump(result, file)

size_json = os.path.getsize(result_json)
size_msgpack = os.path.getsize(result_msgpack)

print(f"Размер файла JSON: {size_json} байт")
print(f"Размер файла MessagePack: {size_msgpack} байт")