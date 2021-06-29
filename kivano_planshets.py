from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano_products.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/planshety'
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}


def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'item product_listbox oh')
    planshet_list = []

    for item in items:
        planshet_list.append({
            'title' : item.find('div', class_ = 'listbox_title oh').get_text(strip = True),
            'product_text' : item.find('div', class_ = 'product_text').get_text(strip = True),
            'price': item.find('div', class_ = 'listbox_price').get_text(strip = True),
            'link' : item.find('div', class_ = 'listbox_title oh').find('a').get('href'),
        })
    return planshet_list

def planshet_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование', 'Описание','Стоимость','Ссылка'])
        for items in items:
            writer.writerow([items['title'],items['product_text'], items['price'], items['link']])

def parse():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        planshet_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            planshet_list.extend(get_content(html.text))
        planshet_save(planshet_list, CSV)
        print('Парсинг готов')
    else:
        print('Error')
 
parse()
