import numpy as np
import os

input_file = 'second_task.npy'
output_file = 'result_2'

try:
    matrix = np.load(input_file)
except FileNotFoundError:
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

indices = np.where(matrix > 503)

x, y = indices  # Индексы по осям
z = matrix[indices]  # Значения элементов

#Сохранение в обычном формате
np.savez(f"{output_file}.npz", x=x, y=y, z=z)

#Сохранение в сжатом формате
np.savez_compressed(f"{output_file}_compressed.npz", x=x, y=y, z=z)

size_normal = os.path.getsize(f"{output_file}.npz")
size_compressed = os.path.getsize(f"{output_file}_compressed.npz")

print(f"Размер обычного файла: {size_normal} байт")
print(f"Размер сжатого файла: {size_compressed} байт")