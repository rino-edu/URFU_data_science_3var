from collections import Counter
import os
import json
from bs4 import BeautifulSoup

def parse_object(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    item={}
    item['title'] = soup.title.string.split('|')[0].strip()
    item['price'] = float(soup.find("div", attrs={'class':'nofloat rmy'}).find("div", attrs={'class':'price'}).find("strong").get_text().strip().replace(' ', ''))

    availability_parent = soup.find("div", attrs={'class':'self'})
    if availability_parent.find("div", attrs={'class':'addr'}):
        item['availability'] = availability_parent.find("div", attrs={'class':'addr'}).find("strong").get_text()
    else:
        item['availability'] = availability_parent.find("div").get_text().split(":")[1].strip().replace("\n", "")

    properties = soup.find("div", attrs={'class':'properties clearfix'}).find_all("dl", attrs={'class':'item'})
    for prop in properties:
        key = prop.find('dt').get_text().strip()
        value = prop.find('dd').get_text().strip()
        if key == "Артикул":
            item['article'] = int(value)
        elif key == "Бренд":
            item['brand'] = value
        elif key == "Страна производитель":
            item['country'] = value
    
    return item

def parse_catalog(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find("section", attrs={'class':'catalog2'}).find_all('figure')
    items=[]

    for product in products:
        item={}
        item['title'] = product.find("div", attrs={'class':'title'}).find('a').get_text().strip()
        props = product.find("div", attrs={'class':'nofloat'}).find('p').get_text()
        item['country'] = props.split("\n")[1].strip()
        item['article'] = int(props.split(":")[1].strip())
        item['availability'] = product.find('span', attrs={'class':'ostatok'}).get_text().split(':')[1].strip()
        item['price'] = float(product.find('div', attrs={'class':'price'}).find('strong').get_text().strip().replace(' ', ''))
        items.append(item)
    
    return items

def parse_html_files(one_page_directory, catalogs_directory):
  all_data = []
  for filename in os.listdir(one_page_directory):
    if filename.endswith(".html"):
      filepath = os.path.join(one_page_directory, filename)
      try:
        data = parse_object(filepath)
        all_data.append(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  
  for filename in os.listdir(catalogs_directory):
    if filename.endswith(".html"):
      filepath = os.path.join(catalogs_directory, filename)
      try:
        data = parse_catalog(filepath)
        all_data.extend(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
      
  return all_data


def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "average": sum(values) / len(values) if values else 0,
        "count": len(values),
    }

def save_results(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

catalog_folder = "5/catalog"
object_folder = "5/object"
output_all_products = "5_result.json"
output_filtered = "5_filtered.json"
output_stats = "5_stat.json"
output_frequency = "5_frequency.json"


all_data = parse_html_files(object_folder, catalog_folder)
sorted_data = sorted(all_data, key=lambda x: x.get("price", 0))

filtered_data = [item for item in sorted_data if item["country"] == "Россия"]

reviews_stats = calculate_statistics(sorted_data, "price")

brands = [item["brand"] for item in sorted_data if "brand" in item]
brands_counts = Counter(brands)

save_results(sorted_data, output_all_products)
save_results(filtered_data, output_filtered)
save_results(reviews_stats, output_stats)
save_results(brands_counts, output_frequency)

print("Результаты сохранены в файлы 5_...")