import requests
from bs4 import BeautifulSoup
import json

news_list = []

for i in range(1, 7):
    url = f'https://pavlodarnews.kz/tag/politsiya?page={i}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.find_all('div', class_='post-item')

    # Проверяем, что на странице есть новости
    if len(news_items) == 0:
        break

    for news_item in news_items:
        # Получаем заголовок новости
        title = news_item.find('h3', class_='title').text.strip()

        # Получаем описание новости
        description = news_item.find('p', class_='description').text.strip()

        # Получаем дату
        date = news_item.find('p', class_='post-meta').text.strip()



        # Получаем ссылку на новость
        link = news_item.find('h3', class_='title').find('a')['href']

        # Получаем ссылку на изображение новости
        img_src = news_item.find('img')['src']


        # Создаем словарь с данными о новости
        new_dict = {'title': title, 'description': description, 'link': link, 'image': img_src, 'date': date}

        # Добавляем словарь в список новостей
        news_list.append(new_dict)

# Сохраняем список новостей в JSON файл
with open('news.json', 'w') as f:
    json.dump(news_list, f)