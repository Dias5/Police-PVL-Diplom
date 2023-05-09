import sqlite3
import json

# Подключаемся к базе данных
conn = sqlite3.connect('police.db')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''CREATE TABLE IF NOT EXISTS News
                  (id INTEGER PRIMARY KEY,
                   title TEXT,
                   description TEXT,
                   image TEXT,
                   link)''')

# Открываем файл с данными
with open('news.json', 'r') as f:
    news_list = json.load(f)

# Записываем данные в базу данных
for news in news_list:
    title = news['title']
    description = news['description']
    image_src = news['image']
    link = news['link']

    # Делаем INSERT запрос к таблице
    cursor.execute('INSERT INTO news (title, description, image, link) VALUES (?, ?, ?, ?)', (title, description, image_src, link))

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()