from collections import Counter
import string
import os

input_file = 'first_task.txt'

# Проверка
if not os.path.exists(input_file):
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

with open(input_file, 'r', encoding='utf-8') as file:
    text = file.read()

# Проверка
if not text.strip():
    print(f"Ошибка: файл '{input_file}' пуст.")
    exit()

# Очистка текста от знаков препинания и перевод в нижний регистр
text_clean = text.translate(str.maketrans('', '', string.punctuation)).lower()
words = text_clean.split()

# Подсчет частоты
word_counts = Counter(words)


# Сохранение в файл
output_file = 'word_frequency.txt'
with open(output_file, 'w', encoding='utf-8') as output_file:
    for word, freq in word_counts.items():
        output_file.write(f"{word}:{freq}\n")

# Вариантная часть: подсчет слов длиной [1, 5]
total_words = len(words)
short_words = [word for word in words if 1 <= len(word) <= 5]
short_word_count = len(short_words)
short_word_ratio = short_word_count / total_words

stats_file = 'short_word_stats.txt'
with open(stats_file, 'w', encoding='utf-8') as stats_file:
    stats_file.write(f"Число коротких слов: {short_word_count}\n")
    stats_file.write(f"Доля коротких слов: {short_word_ratio:.2%}\n")

print(f"Частота слов сохранена в '{output_file.name}'.")
print(f"Статистика по коротким словам сохранена в '{stats_file.name}'.")