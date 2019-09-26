import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    links = []

    for td in tds:
        a = td.find('a', class_='currency-name-container link-secondary').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='details-panel-item--name').text.strip()
    except:
        name = ''
    try:
        price = soup.find('spa', class_='h2 text-semi-bold details-panel-item--price__value').text.strip()
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['name'],
                          data['price']) )
        print(data['name'], 'parsed')
def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

    with Pool(40) as p:
        p.map(make_all, all_links)
    #for url in all_links:
        #html = get_html(url)
        #data = get_page_data(html)
        #write_csv(data)
    #end = datetime.now()
    #total = end - start
    #print(str(total))

if __name__ == '__main__':
    main()
