import pandas as pd

input_file = 'fourth_task.csv'

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

#Удаление столбца rating
if "rating" in df.columns:
    df = df.drop(columns=["rating"])
else:
    print("Предупреждение: столбец 'rating' отсутствует в файле.")

#Найти среднее по price
if "price" in df.columns:
    mean_price = df["price"].mean()
else:
    print("Ошибка: столбец 'price' отсутствует.")
    exit()

#Найти максимум по quantity
if "quantity" in df.columns:
    max_quantity = df["quantity"].max()
else:
    print("Ошибка: столбец 'quantity' отсутствует.")
    exit()

#Найти минимум по price
if "price" in df.columns:
    min_price = df["price"].min()
else:
    print("Ошибка: столбец 'price' отсутствует.")
    exit()

#Фильтрация значений, где status != Refunded
if "status" in df.columns:
    df_filtered = df[df["status"] != "Refunded"]
else:
    print("Ошибка: столбец 'status' отсутствует.")
    exit()


results_file = 'results.txt'
with open(results_file, 'w', encoding='utf-8') as file:
    file.write(f"{mean_price}\n")
    file.write(f"{max_quantity}\n")
    file.write(f"{min_price}")

output_file = 'modified_fourth_task.csv'
df_filtered.to_csv(output_file, index=False)

print(f"Результаты вычислений сохранены в '{results_file}'.")
print(f"Модифицированный файл сохранен в '{output_file}'.")