import os
import json
from bs4 import BeautifulSoup
from collections import Counter

def parse_clothing(clothing):
    item = {}

    item["id"] = int(clothing.id.get_text())
    item["name"] = clothing.find_all('name')[0].get_text().strip()
    item["category"] = clothing.category.get_text().strip()
    item["size"] = clothing.size.get_text().strip()
    item["color"] = clothing.color.get_text().strip()
    item["material"] = clothing.material.get_text().strip()
    item["price"] = float(clothing.price.get_text().strip())
    item["rating"] = float(clothing.rating.get_text().strip())
    item["reviews"] = int(clothing.reviews.get_text().strip())

    if clothing.sporty is not None:
        item["sporty"] = clothing.sporty.get_text().strip() == "yes"
    if clothing.new is not None:
        item["new"] = clothing.new.get_text().strip() == "+"
    if clothing.exclusive is not None:
        item["exclusive"] = clothing.exclusive.get_text().strip() == "yes"

    return item

def parse_all_files(input_folder):
    all_data = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                xml_content = file.read()

            soup = BeautifulSoup(xml_content, "xml")
            for clothing in soup.find_all("clothing"):
                clothing_data = parse_clothing(clothing)
                all_data.append(clothing_data)

    return all_data

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "average": sum(values) / len(values) if values else 0,
        "count": len(values),
    }


input_folder = "4"
output_all_stars = "4_result.json"
output_filtered = "4_filtered.json"
output_stats = "4_stat.json"
output_frequency = "4_frequency.json"

all_data = parse_all_files(input_folder)

sorted_data = sorted(all_data, key=lambda x: x.get("price", 0))

filtered_data = [item for item in sorted_data if item.get("sporty")]

reviews_stats = calculate_statistics(sorted_data, "reviews")

categories = [item["category"] for item in sorted_data if "category" in item]
category_counts = Counter(categories)

save_results(sorted_data, output_all_stars)
save_results(filtered_data, output_filtered)
save_results(reviews_stats, output_stats)
save_results(category_counts, output_frequency)

print("Результаты сохранены в файлы 4_...")