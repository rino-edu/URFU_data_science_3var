import os

input_file = 'second_task.txt'

if not os.path.exists(input_file):
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

if not lines:
    print(f"Ошибка: файл '{input_file}' пуст.")
    exit()

#Функция для обработки строки
def process_line(line):
    numbers = map(int, line.split())
    filtered_numbers = [abs(num) for num in numbers if num ** 2 <= 100_000]
    return sum(filtered_numbers)

#Операция для строки
sums = [process_line(line) for line in lines]

#Операция для столбца
sorted_sums = sorted(sums, reverse=True)
top_10_sums = sorted_sums[:10]

output_file = 'top_sums.txt'

with open(output_file, 'w', encoding='utf-8') as file:
    for top_sum in top_10_sums:
        file.write(f"{top_sum}\n")

print(f"Топ-10 сумм сохранены в '{output_file}'.")
