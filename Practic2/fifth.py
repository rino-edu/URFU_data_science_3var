import pandas as pd
import json
import msgpack
import pickle
import os

input_file = 'anime.csv'
output_base_name = 'result_5'

try:
    data = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Ошибка: файл '{input_file}' не найден.")
    exit()

selected_fields = ['source', 'type', 'score', 'scored_by', 'status', 'episodes', 'members']
data = data[selected_fields]

numerical_fields = ['score', 'scored_by', 'episodes', 'members']
text_fields = ['source', 'type', 'status']

for field in numerical_fields:
    if field in data.columns:
        data[field] = pd.to_numeric(data[field], errors='coerce')

numerical_stats = {}
for field in numerical_fields:
    if field in data.columns:
        numerical_stats[field] = {
            "max": data[field].max(),
            "min": data[field].min(),
            "mean": data[field].mean(),
            "sum": data[field].sum(),
            "std_dev": data[field].std()
        }

for field in numerical_stats:
    for stat in numerical_stats[field]:
        numerical_stats[field][stat] = (
            numerical_stats[field][stat].item() if pd.notna(numerical_stats[field][stat]) else None
        )

text_stats = {}
for field in text_fields:
    if field in data.columns:
        text_stats[field] = data[field].value_counts().to_dict()

calc_file_path = f"{output_base_name}_calc.json"
with open(calc_file_path, "w", encoding="utf-8") as json_file:
    json.dump({"numerical_stats": numerical_stats, "text_stats": text_stats}, json_file, indent=4, ensure_ascii=False)

# CSV
csv_file_path = f"{output_base_name}.csv"
data.to_csv(csv_file_path, index=False)

# JSON
json_file_path = f"{output_base_name}.json"
data.to_json(json_file_path, orient="records", lines=True)

# MessagePack
msgpack_file_path = f"{output_base_name}.msgpack"
with open(msgpack_file_path, "wb") as msgpack_file:
    msgpack.dump(data.to_dict(orient="records"), msgpack_file)

# Pickle
pkl_file_path = f"{output_base_name}.pkl"
with open(pkl_file_path, "wb") as pickle_file:
    pickle.dump(data, pickle_file)

file_sizes = {
    "CSV": os.path.getsize(csv_file_path),
    "JSON": os.path.getsize(json_file_path),
    "MessagePack": os.path.getsize(msgpack_file_path),
    "Pickle": os.path.getsize(pkl_file_path),
    "Analysis JSON": os.path.getsize(calc_file_path)
}
print("Размеры файлов:")
for format_name, size in file_sizes.items():
    print(f"{format_name}: {size / 1024:.2f} KB")

print("Файлы успешно созданы и сохранены.")