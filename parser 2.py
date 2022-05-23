import requests
from bs4 import BeautifulSoup
import csv

FILE = 'cars.csv'
HOST = 'https://auto.ria.com'
URL = 'https://auto.ria.com/uk/newauto/marka-renault/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}


def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS,  params=params)
    return response

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='proposition')
    cars = []

    for item in items:
        cars.append(
            {
                'title': item.find('h3', class_='proposition_name').get_text(strip=True),
                'link': HOST + item.find('a', class_='proposition_link').get('href'), # href нужен что бы выдавало в виде ссылки
                'cost_USD': item.find('span', class_='green bold size22').get_text(strip=True),
                'cost_UAH': item.find('span', class_='size16').get_text(strip=True),
                'city': item.find('span', class_='item region').get_text(strip=True),
                'car_img': item.find('div', class_='photo-car').find('img').get('src')
                #выбираем большой класс где хранятся картинки photo-car, ищем подклас img, src- говорит что нужно найти путь к картинке
            }
        )
    return cars

def save_document(items, path):
    with open(path, 'w',  encoding='utf-16', newline='') as file:
        writer = csv.writer(file, delimiter=';') # ; легко читает эксель
        writer.writerow(['Название машины', "Ссылка на товар", "Цена в долларах", "Цена в гривне", "Город", "Фото"])  # заголовки колонок
        for item in items:
            writer.writerow([item['title'], item['link'], item['cost_USD'], item['cost_UAH'], item['city'], item['car_img']])

def parser():
    PAGENATION = input('Введите количество страниц для парсинга:')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code ==200:
        cars = []
        for page in range(1, PAGENATION + 1):
            print(f'Парсим страницу {page} из {PAGENATION}')
            html = get_html(URL, params={'page': page})
            # params=  - название аргумента который мы указывали ранее {'page' - берем в ссылке на второй странице : page - значение аргумента из цикла фор }
            cars.extend(get_content(html.text))
            save_document(cars, FILE)
    else:
        print('Error')

parser()