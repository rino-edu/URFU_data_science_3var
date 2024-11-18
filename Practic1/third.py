import os
import numpy as np

input_file = 'third_task.txt'

if not os.path.exists(input_file):
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

if not lines:
    print(f"Ошибка: файл '{input_file}' пуст.")
    exit()

# Функция для замены N/A
def replace_na_with_mean(line):
    numbers = []
    for value in line.split():
        if value.upper() == "N/A":
            numbers.append(np.nan)
        else:
            numbers.append(float(value))
    numbers = np.array(numbers)

    for i in range(len(numbers)):
        if np.isnan(numbers[i]):
            left = numbers[i - 1] if i > 0 else 0
            right = numbers[i + 1] if i < len(numbers) - 1 else 0
            neighbors = [x for x in [left, right] if not np.isnan(x)]
            numbers[i] = np.mean(neighbors)
    return list(map(int, numbers))

# Функция фильтрации данных
def filter_line(numbers):
    filtered = [num for num in numbers if num % 2 != 0 and num <= 500]
    return filtered if filtered else [0]

result_sums = []
for line in lines:
    replaced_numbers = replace_na_with_mean(line)

    filtered_numbers = filter_line(replaced_numbers)

    line_sum = sum(filtered_numbers)

    result_sums.append(line_sum)

output_file = '3_result.txt'

with open(output_file, 'w', encoding='utf-8') as file:
    for line_sum in result_sums:
        file.write(f"{line_sum}\n")

print(f"Суммы по строкам сохранены в '{output_file}'.")
