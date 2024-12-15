import os
import json
import re
from bs4 import BeautifulSoup
from statistics import mean, stdev

def parse_product(product):
    data = {}

    img = product.find("img")
    if img and "src" in img.attrs:
        data["image"] = img["src"]

    details = product.find("span")
    if details:
        match = re.search(r'(\d+\.\d+)"\s(.+?)\s(\d+)GB', details.text.strip())
        if match:
            data["size"] = float(match.group(1))
            data["brand"] = match.group(2)
            data["memory_size"] = int(match.group(3))

    price = product.find("price")
    if price:
        data["price"] = int(re.sub(r"[^\d]", "", price.text))

    bonuses = product.find("strong")
    if bonuses:
        match = re.search(r"\d+", bonuses.text)
        if match:
            data["bonuses"] = int(match.group())

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

def sort_by_field(data, field):
    return sorted(data, key=lambda x: x.get(field, float("inf")))

def filter_by_field(data, field, threshold):
    return [item for item in data if field in item and item[field] > threshold]

def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "std_dev": stdev(values) if len(values) > 1 else 0,
        "count": len(values)
    }

def calculate_frequency(data, field):
    frequency = {}
    for item in data:
        if field in item:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency

input_folder = "2"
output_all_products = "2_result.json"
output_filtered = "2_filtered.json"
output_stats = "2_stat.json"
output_frequency = "2_frequency.json"

all_data = parse_all_files(input_folder)

# Сортировка по price
sorted_data = sort_by_field(all_data, "price")
with open(output_all_products, "w", encoding="utf-8") as file:
    json.dump(sorted_data, file, ensure_ascii=False, indent=4)

# Фильтрация по memory_size > 100
filtered_data = filter_by_field(all_data, "memory_size", 100)
with open(output_filtered, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

# Статистика для memory_size
statistics = calculate_statistics(all_data, "memory_size")
with open(output_stats, "w", encoding="utf-8") as file:
    json.dump(statistics, file, ensure_ascii=False, indent=4)

# Частота меток для brand
frequency = calculate_frequency(all_data, "brand")
with open(output_frequency, "w", encoding="utf-8") as file:
    json.dump(frequency, file, ensure_ascii=False, indent=4)

print("Результаты сохранены в файлы 2_...")