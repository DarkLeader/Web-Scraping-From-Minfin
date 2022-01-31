import requests
from bs4 import BeautifulSoup
import csv
CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
#es funqcia igebs htmls da parametrebs
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='be80pr-15 kwXsZB').get_text(strip=True),
                'link_product': item.find('div', class_='be80pr-15 kwXsZB').find('a').get('href'),
                'brand': item.find('span', class_='be80pr-21 dksWIi').get_text(strip=True),
                'card_img': item.find('div', class_='be80pr-9 fJFiLL').find('img').get('src')

            }
        )
    return cards
def save_doc(items, path):
    with open(path, 'w', newline='') as file :
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name of product', 'link of product', 'bank', 'card image'])
        for item in items:
            writer.writerow( [item['title'], item['link_product'], item['brand'], item['card_img']])
#am funqcias vatant htmls da igebs konkretul kontents migebuli html-dan
def parser():
    PAGENATION = input('Type amount of pages for parsing: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Parsing page: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')
parser()
 
