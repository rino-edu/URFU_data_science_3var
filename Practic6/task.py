import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def read_file(file_name):
    return pd.read_csv(file_name, sep=';')

def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f"file in memory size = {total_memory_usage // 1024:10} КБ")
    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": float(memory_usage_stat[key] // 1024),
            "memory_per": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": str(df.dtypes[key])
        })
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    for column in column_stat:
        print(
            f"{column['column_name']:15}: {int(column['memory_abs']):10} КБ: {column['memory_per']:10}% : {column['dtype']}")
    return column_stat


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # предположим, что если это не датафрейм, то серия
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # преобразуем байты в мегабайты
    return "{:03.2f} MB".format(usage_mb)


def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))
    return converted_obj

def opt_int(df):
    dataset_int = df.select_dtypes(include=['int'])
    """
    downcast:
            - 'integer' or 'signed': smallest signed int dtype (min.: np.int8)
            - 'unsigned': smallest unsigned int dtype (min.: np.uint8)
            - 'float': smallest float dtype (min.: np.float32)
    """
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')
    print(mem_usage(dataset_int))
    print(mem_usage(converted_int))
    #
    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int


def opt_float(df):
    # # =======================================================================
    # # выполняем понижающее преобразование
    # # для столбцов типа float
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float


file_name = "Russia_Real_Estate_2021.csv"
dataset = read_file(file_name)

non_optimized_stat = get_memory_stat_by_column(dataset)

with open('non_optimized_stat.json', 'w', encoding='utf-8') as f:
    json.dump(non_optimized_stat, f, ensure_ascii=False, indent=4)


optimized_dataset = dataset.copy()

converted_obj = opt_obj(dataset)
converted_int = opt_int(dataset)
converted_float = opt_float(dataset)

optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

print(mem_usage(dataset))
print(mem_usage(optimized_dataset))
optimized_dataset.info(memory_usage='deep')

optimized_stat = get_memory_stat_by_column(optimized_dataset)

with open('optimized_stat.json', 'w', encoding='utf-8') as f:
    json.dump(optimized_stat, f, ensure_ascii=False, indent=4)

need_column = dict()
column_names = ['date', 'price', 'level',
                 'levels', 'rooms', 'area',
                 'geo_lat', 'geo_lon', 'id_region', 'building_type']

opt_dtypes = optimized_dataset.dtypes
for key in dataset.columns:
    need_column[key] = opt_dtypes[key]
    print(f"{key}:{opt_dtypes[key]}")

with open("dtypes.json", mode="w") as file:
    dtype_json = need_column.copy()
    for key in dtype_json.keys():
        dtype_json[key] = str(dtype_json[key]) 

    json.dump(dtype_json, file)

read_and_optimized = pd.read_csv(file_name, usecols=lambda x: x in column_names, dtype=need_column, sep=';')
print(read_and_optimized)

get_memory_stat_by_column(read_and_optimized)


    
def figure1(read_and_optimized):
  plt.figure(figsize=(10, 6))
  sns.countplot(x='rooms', data=read_and_optimized)
  plt.title('Количество квартир в зависимости от количества комнат')
  plt.xlabel('Количество комнат')
  plt.ylabel('Количество квартир')
  plt.show()


def figure2(read_and_optimized):
  plt.figure(figsize=(10, 6))
  sns.scatterplot(x='area', y='price', data=read_and_optimized)
  plt.title('Корреляция между ценой и площадью квартиры')
  plt.xlabel('Площадь (кв.м)')
  plt.ylabel('Цена')
  plt.show()


def figure3(read_and_optimized):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='levels', y='price', data=read_and_optimized, showfliers=False, palette='coolwarm')
    plt.title('Зависимость цены от этажности здания')
    plt.xlabel('Этажность здания')
    plt.ylabel('Цена')
    plt.show()

def figure4(read_and_optimized):
    bins = [0, 5, 10, 15, 20, 50]
    labels = ['1-5 этажей', '6-10 этажей', '11-15 этажей', '16-20 этажей', '21+ этажей']
    
    read_and_optimized['levels_grouped'] = pd.cut(read_and_optimized['levels'], bins=bins, labels=labels, right=False)
    
    levels_counts = read_and_optimized['levels_grouped'].value_counts()
    
    plt.figure(figsize=(8, 8))
    plt.pie(levels_counts, labels=levels_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Доля квартир по этажности здания')
    plt.axis('equal')
    plt.show()

def figure5(read_and_optimized):
    avg_price_by_region = read_and_optimized.groupby('id_region')['price'].mean().sort_values(ascending=False)
    plt.figure(figsize=(12, 8))
    avg_price_by_region.plot(kind='bar', color='skyblue')
    plt.title('Средняя цена квартиры по регионам')
    plt.xlabel('ID региона')
    plt.ylabel('Средняя цена')
    plt.show()

def figure6(read_and_optimized):
    rooms_counts = read_and_optimized['rooms'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(
        rooms_counts, 
        labels=rooms_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=sns.color_palette('pastel')
    )
    plt.title('Доля квартир по количеству комнат')
    plt.axis('equal')
    plt.show()

figure1(read_and_optimized)
figure2(read_and_optimized)
figure4(read_and_optimized)
figure5(read_and_optimized)
figure6(read_and_optimized)