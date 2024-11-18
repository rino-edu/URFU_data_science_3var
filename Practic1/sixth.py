import requests

url = 'https://api.hh.ru/vacancies'

params = {
    'text': 'Flutter',
    'per_page': 5
}

# Фетчим вакансии с hh.ru в json
def fetch_vacancies():
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе: {response.status_code}")
        return None

# Генерируем HTML
def generate_html(vacancies):
    if 'items' not in vacancies:
        print("Нет данных для генерации HTML.")
        return ""

    # Начало HTML-документа
    html_content = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Вакансии Flutter</title>
    </head>
    <body>
        <h1>Список вакансий</h1>
        <ul>
    '''

    # Перебор вакансий
    for vacancy in vacancies['items']:
        name = vacancy.get('name', 'Название не указано')
        employer = vacancy.get('employer', {}).get('name', 'Работодатель не указан')
        salary = vacancy.get('salary')
        salary_from = salary.get('from') if salary else 'Не указана'
        salary_to = salary.get('to') if salary else 'Не указана'
        salary_currency = salary.get('currency') if salary else ''
        area = vacancy.get('area', {}).get('name', 'Регион не указан')
        published_at = vacancy.get('published_at', 'Дата не указана')
        url = vacancy.get('alternate_url', '#')

        html_content += f'''
        <li>
            <h2><a href="{url}" target="_blank">{name}</a></h2>
            <p><strong>Работодатель:</strong> {employer}</p>
            <p><strong>Зарплата:</strong> от {salary_from} до {salary_to} {salary_currency}</p>
            <p><strong>Регион:</strong> {area}</p>
            <p><strong>Дата публикации:</strong> {published_at}</p>
        </li>
        '''

    # Завершение HTML-документа
    html_content += '''
        </ul>
    </body>
    </html>
    '''

    return html_content

def save_html(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"HTML-файл '{filename}' успешно создан.")

def main():
    vacancies = fetch_vacancies()
    if vacancies:
        html_content = generate_html(vacancies)
        if html_content:
            save_html(html_content, 'vacancies.html')

if __name__ == "__main__":
    main()