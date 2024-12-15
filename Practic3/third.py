import os
import json
from bs4 import BeautifulSoup
from collections import Counter

def parse_star(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    star = BeautifulSoup(xml_content, features="xml").star
    item = {}

    for el in star:
        if el.name is None:
            continue
        item[el.name] = el.get_text().strip()
    
    item['radius'] = int(item["radius"])

    return item

def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "average": sum(values) / len(values) if values else 0,
        "count": len(values),
    }

input_folder = "3"
output_all_stars = "3_result.json"
output_filtered = "3_filtered.json"
output_stats = "3_stat.json"
output_frequency = "3_frequency.json"

all_stars = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xml"):
        file_path = os.path.join(input_folder, file_name)
        star_data = parse_star(file_path)
        all_stars.append(star_data)

# Сортировка
all_stars_sorted = sorted(all_stars, key=lambda x: x["radius"])

with open(output_all_stars, "w", encoding="utf-8") as file:
    json.dump(all_stars_sorted, file, ensure_ascii=False, indent=4)

# Фильтрация звезд только в созвездии "Стрелец"
filtered_stars = [star for star in all_stars_sorted if star["constellation"] and star["constellation"] in "Стрелец"]
with open(output_filtered, "w", encoding="utf-8") as file:
    json.dump(filtered_stars, file, ensure_ascii=False, indent=4)

# Статистические характеристики для параметра "radius"
radius_stats = calculate_statistics(all_stars_sorted, "radius")
with open(output_stats, "w", encoding="utf-8") as file:
    json.dump(radius_stats, file, ensure_ascii=False, indent=4)

# Частота меток для созвездий
constellations = [star["constellation"] for star in all_stars if "constellation" in star]
constellation_frequency = Counter(constellations)
with open(output_frequency, "w", encoding="utf-8") as file:
    json.dump(constellation_frequency, file, ensure_ascii=False, indent=4)

print("Результаты сохранены в файлы 3_...")