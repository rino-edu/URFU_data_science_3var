from bs4 import BeautifulSoup
import pandas as pd
import os

input_file = 'fifth_task.html'

if not os.path.exists(input_file):
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

with open(input_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

#Парсинг HTML с помощью BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

#Поиск таблицы по ID (если известно) или первым вхождением <table>
table = soup.find('table', id='product-table')
if not table:
    print("Ошибка: таблица не найдена в HTML-файле.")
    exit()

#Извлечение заголовков
headers = [header.get_text(strip=True) for header in table.find_all('th')]

# Извлечение строк таблицы
rows = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells]
    rows.append(row_data)

df = pd.DataFrame(rows, columns=headers)

output_file = '5_result.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"Данные из HTML-таблицы успешно сохранены в '{output_file}'.")