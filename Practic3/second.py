import os
import json
import re
from bs4 import BeautifulSoup
from statistics import mean, stdev

def parse_product(product):
    data = {}

    # Парсинг изображения
    img = product.find("img")
    if img and "src" in img.attrs:
        data["image"] = img["src"]

    # Парсинг характеристик из строки (size, brand, memory_size)
    details = product.find("span")
    if details:
        match = re.search(r'(\d+\.\d+)"\s(.+?)\s(\d+)GB', details.text.strip())
        if match:
            data["size"] = float(match.group(1))
            data["brand"] = match.group(2)
            data["memory_size"] = int(match.group(3))

    # Парсинг цены
    price = product.find("price")
    if price:
        data["price"] = int(re.sub(r"[^\d]", "", price.text))

    # Парсинг бонусов
    bonuses = product.find("strong")
    if bonuses:
        match = re.search(r"\d+", bonuses.text)
        if match:
            data["bonuses"] = int(match.group())

    # Парсинг дополнительных характеристик
    for li in product.find_all("li"):
        type_attr = li.get("type")
        if type_attr:
            value = li.text.strip()
            if type_attr == "processor":
                match = re.search(r"(\d+)x([\d\.]+) ГГц", value)
                if match:
                    data["processor_cores"] = int(match.group(1))
                    data["processor_speed"] = float(match.group(2))
            elif type_attr == "ram":
                data["ram"] = int(re.sub(r"[^\d]", "", value))
            elif type_attr == "sim":
                data["sim_count"] = int(re.sub(r"[^\d]", "", value))
            elif type_attr == "resolution":
                data["resolution"] = value
            elif type_attr == "camera":
                data["camera"] = int(re.sub(r"[^\d]", "", value))
            elif type_attr == "acc":
                data["battery"] = int(re.sub(r"[^\d]", "", value))

    return data

# Функция для парсинга всех файлов в папке
def parse_all_files(input_folder):
    all_products = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                products = soup.find_all("div", class_="product-item")

                for product in products:
                    product_data = parse_product(product)
                    if product_data:
                        all_products.append(product_data)

    return all_products

# Функция для сортировки записей по полю
def sort_by_field(data, field):
    return sorted(data, key=lambda x: x.get(field, float("inf")))

# Функция для фильтрации записей по полю
def filter_by_field(data, field, threshold):
    return [item for item in data if field in item and item[field] > threshold]

# Функция для расчета статистики числового поля
def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "stdev": stdev(values) if len(values) > 1 else 0
    }

# Функция для подсчета частоты меток текстового поля
def calculate_frequency(data, field):
    frequency = {}
    for item in data:
        if field in item:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency

# Основная функция
if __name__ == "__main__":
    input_folder = "2"

    # Парсинг данных
    all_data = parse_all_files(input_folder)

    # Сохранение всех данных
    with open("2_result.json", "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    # Сортировка по цене
    sorted_data = sort_by_field(all_data, "price")
    with open("2_sorted.json", "w", encoding="utf-8") as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)

    # Фильтрация по memory_size > 100
    filtered_data = filter_by_field(all_data, "memory_size", 100)
    with open("2_filtered.json", "w", encoding="utf-8") as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    # Статистика для memory_size
    statistics = calculate_statistics(all_data, "memory_size")
    with open("2_stat.json", "w", encoding="utf-8") as file:
        json.dump(statistics, file, ensure_ascii=False, indent=4)

    # Частота меток для brand
    frequency = calculate_frequency(all_data, "brand")
    with open("2_frequency.json", "w", encoding="utf-8") as file:
        json.dump(frequency, file, ensure_ascii=False, indent=4)

    print("Задание выполнено. Результаты сохранены в файлы.")
