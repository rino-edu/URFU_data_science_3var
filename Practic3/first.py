import os
import json
from bs4 import BeautifulSoup
from statistics import mean, stdev

def parse_book(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    item = {}

    item["title"] = soup.find("h1", {"class": "book-title"}).get_text(strip=True) if soup.find("h1", {"class": "book-title"}) else None
    item["author"] = soup.find_all("p", {"class": "author-p"})[0].get_text(strip=True) if soup.find_all("p", {"class": "author-p"}) else None

    category = soup.find("span", string=lambda x: x and "Категория:" in x)
    item["category"] = category.get_text(strip=True).replace("Категория:", "").strip() if category else None

    pages = soup.find("span", {"class": "pages"})
    item["pages"] = int(pages.get_text().split(":")[1].split()[0]) if pages else None

    year = soup.find("span", {"class": "year"})
    item["year"] = int(year.get_text().split("в")[1].strip()) if year else None

    isbn = soup.find("span", string=lambda x: x and "ISBN:" in x)
    item["isbn"] = isbn.get_text().split(":")[1].strip() if isbn else None

    description = soup.find("p", string=lambda x: x and "Описание" in x)
    item["description"] = description.get_text().split("Описание")[1].strip() if description else None

    rating = soup.find("span", string=lambda x: x and "Рейтинг:" in x)
    item["rating"] = float(rating.get_text().split(":")[1].strip()) if rating else None

    views = soup.find("span", string=lambda x: x and "Просмотры:" in x)
    item["views"] = int(views.get_text().split(":")[1].strip()) if views else None

    image = soup.find("img")
    item["image"] = image["src"] if image else None

    return item

input_folder = "1"
output_all_books = "1_result.json"
output_filtered = "1_filtered.json"
output_stats = "1_stat.json"
output_frequency = "1_frequency.json"

all_books = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        file_path = os.path.join(input_folder, file_name)
        book_data = parse_book(file_path)
        all_books.append(book_data)

# Сортировка
all_books_sorted = sorted(all_books, key=lambda x: x["year"])

with open(output_all_books, "w", encoding="utf-8") as file:
    json.dump(all_books_sorted, file, ensure_ascii=False, indent=4)

# Фильтрация книг с рейтингом выше 4.0
filtered_books = [book for book in all_books if book["rating"] and book["rating"] > 4.0]
with open(output_filtered, "w", encoding="utf-8") as file:
    json.dump(filtered_books, file, ensure_ascii=False, indent=4)

# Статистические характеристики для параметра "pages"
pages = [book["pages"] for book in all_books if book["pages"] is not None]
pages_stats = {
    "sum": sum(pages),
    "min": min(pages),
    "max": max(pages),
    "mean": mean(pages),
    "std_dev": stdev(pages) if len(pages) > 1 else 0,
    "count": len(pages)
}
with open(output_stats, "w", encoding="utf-8") as file:
    json.dump(pages_stats, file, ensure_ascii=False, indent=4)

# Частота меток для параметра "Категория"
categories = [book["category"] for book in all_books if book["category"]]
category_frequency = {cat: categories.count(cat) for cat in set(categories)}
with open(output_frequency, "w", encoding="utf-8") as file:
    json.dump(category_frequency, file, ensure_ascii=False, indent=4)

print("Результаты сохранены в файлы 1_...")