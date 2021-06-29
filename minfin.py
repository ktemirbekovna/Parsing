from bs4 import BeautifulSoup
import requests
import csv

CSV = 'minfin_news.csv'
HOST = 'http://www.minfin.kg/ru/'
URL = 'http://www.minfin.kg/ru/novosti/mamlekettik-karyz/gosudarstvennyy-dolg'
HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 

    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}


def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'news')
    news_list = []

    for item in items:
        news_list.append({
            'date': item.find('div', class_ = 'news_date').get_text(strip = True),
            'title' : item.find('div', class_ = 'news_name').get_text(strip = True),
            'link' : item.find('div', class_ = 'news_name').find('a').get('href'),
        })
    return news_list

def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['День публикации', 'Новость','Ссылка'])
        for items in items:
            writer.writerow([items['date'], items['title'], items['link']])

def parse():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            news_list.extend(get_content(html.text))
        news_save(news_list, CSV)
        print('Парсинг готов')
    else:
        print('Error')
 
parse()

