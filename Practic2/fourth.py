import pickle
import json

pkl_file = 'fourth_task_products.pkl'
json_file = 'fourth_task_updates.json'
output_file = 'result_4.pkl'

try:
    with open(pkl_file, 'rb') as file:
        products = pickle.load(file)
except FileNotFoundError:
    print(f"Ошибка: файл '{pkl_file}' не найден.")
    exit()

try:
    with open(json_file, 'r', encoding='utf-8') as file:
        price_updates = json.load(file)
except FileNotFoundError:
    print(f"Ошибка: файл '{json_file}' не найден.")
    exit()

for update in price_updates:
    name = update.get("name")
    method = update.get("method")
    param = update.get("param")

    for product in products:
        if product.get("name") == name:
            old_price = product.get("price", 0)

            if method == "add":
                product["price"] = old_price + param
            elif method == "sub":
                product["price"] = max(0, old_price - param)
            elif method == "percent+":
                product["price"] = old_price * (1 + param)
            elif method == "percent-":
                product["price"] = old_price * (1 - param)

            product["price"] = round(product["price"], 2)

with open(output_file, 'wb') as file:
    pickle.dump(products, file)

print(f"Обновлённые данные сохранены в файл '{output_file}'.")