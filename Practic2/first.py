import numpy as np
import json

input_file = 'first_task.npy'
output_file = 'result_1.json'
normalized_matrix_file = 'normalized_matrix.npy'

try:
    matrix = np.load(input_file)
except FileNotFoundError:
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

#Сумма всех элементов
matrix_sum = np.sum(matrix)

#Ср.арифм. всех элементов
matrix_avg = np.mean(matrix)

#Сумма и среднее главной диагонали
main_diag = np.diagonal(matrix)
sum_main_diag = np.sum(main_diag)
avg_main_diag = np.mean(main_diag)

#Сумма и среднее побочной диагонали
sec_diag = np.diagonal(np.fliplr(matrix))
sum_sec_diag = np.sum(sec_diag)
avg_sec_diag = np.mean(sec_diag)

#Макс и мин
matrix_max = np.max(matrix)
matrix_min = np.min(matrix)

#.item() для преобразования в стандарт-ые типы питона
results = {
    "sum": matrix_sum.item(),
    "avr": matrix_avg.item(),
    "sumMD": sum_main_diag.item(),
    "avrMD": avg_main_diag.item(),
    "sumSD": sum_sec_diag.item(),
    "avrSD": avg_sec_diag.item(),
    "max": matrix_max.item(),
    "min": matrix_min.item()
}

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, indent=4, ensure_ascii=False)
print(f"Результаты вычислений записаны в файл '{output_file}'.")

#Нормализация: (x - min) / (max - min)
normalized_matrix = (matrix - matrix_min) / (matrix_max - matrix_min)
np.save(normalized_matrix_file, normalized_matrix)
print(f"Нормализованная матрица сохранена в файл '{normalized_matrix_file}'.")