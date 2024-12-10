import os
import json
from bs4 import BeautifulSoup
from statistics import mean, stdev

def parse_book(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    title = soup.find("h1", class_="book-title").get_text(strip=True) if soup.find("h1", class_="book-title") else None
    author = soup.find("p", class_="author-p").get_text(strip=True) if soup.find("p", class_="author-p") else None

    category = soup.find("span", string=lambda x: x and "Категория:" in x)
    category = category.get_text(strip=True).replace("Категория:", "").strip() if category else None

    pages = soup.find("span", class_="pages")
    pages = int(pages.get_text(strip=True).replace("Объем:", "").replace("страниц", "").strip()) if pages else None

    year = soup.find("span", class_="year")
    year = int(year.get_text(strip=True).replace("Издано в", "").strip()) if year else None

    isbn = soup.find("span", string=lambda x: x and "ISBN:" in x)
    isbn = isbn.get_text(strip=True).replace("ISBN:", "").strip() if isbn else None

    description = soup.find("p", string=lambda x: x and "Описание" in x)
    description = description.get_text(strip=True).replace("Описание", "").strip() if description else None

    rating = soup.find("span", string=lambda x: x and "Рейтинг:" in x)
    rating = float(rating.get_text(strip=True).replace("Рейтинг:", "").strip()) if rating else None

    views = soup.find("span", string=lambda x: x and "Просмотры:" in x)
    views = int(views.get_text(strip=True).replace("Просмотры:", "").strip()) if views else None

    image = soup.find("img")["src"] if soup.find("img") else None

    return {
        "title": title,
        "author": author,
        "category": category,
        "pages": pages,
        "year": year,
        "isbn": isbn,
        "description": description,
        "rating": rating,
        "views": views,
        "image": image
    }

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

print("Задание выполнено. Результаты сохранены в файлы.")