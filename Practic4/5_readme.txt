Описание ПО: 
Датасет содержит информацию о пиве, пивоварнях, и отзывах пользователей на позиции пива с сервиса UNTAPDD для оценки позиций пива. 

Описание таблиц:

breweries: Содержит информацию о пивоварнях
  brewery_id (INTEGER, PRIMARY KEY): ИД пивоварни
  brewery_name (TEXT): Название

beers: Содержит информацию о позициях пива
  beer_beerid (INTEGER, PRIMARY KEY): ИД пива
  beer_name (TEXT): Название пива
  beer_style (TEXT): Стиль пива
  beer_abv (REAL): Процент алкоголя
  brewery_id (INTEGER): ИД пивоварни

reviews: Содержит информацию об отзывах пользователей на позиции пива
  review_id (INTEGER, PRIMARY KEY AUTOINCREMENT): ИД отзыва
  beer_beerid (INTEGER, FOREIGN KEY referencing Beers): ИД пива
  review_time (INTEGER): Время публикации отзыва (Unix timestamp но хранится простоо в инте)
  review_profilename (TEXT): Ник ревьюера
  review_overall (REAL): Общая оценка
  review_aroma (REAL): Оценка аромата
  review_appearance (REAL): Оценка внешнего вида
  review_palate (REAL): Оценка послевкусия
  review_taste (REAL): Оценка вкуса