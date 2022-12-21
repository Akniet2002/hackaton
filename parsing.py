import csv
import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text 

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('div', class_='pager-wrap').find('ul')
    last_page = pages_ul.find_all('li')[-2]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)

def write_to_csv(data):
    with open('kivano.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                         data['price'],
                         data['photo']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='list-view')
    products = product_list.find_all('div', class_='item product_listbox oh')

    for product in products:
        try:
            photo = product.find('div', class_='listbox_img pull-left').find('a').find('img').get('src')
        except:
            photo = ''

        try:
            title = product.find('div', class_='listbox_title oh').find('a').text.strip()
        except:
            title = ''

        try:
            price = product.find('div', class_='listbox_price text-center').text.strip()
        except:
            price = ''
        
        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)

def main():
    url = f'https://www.kivano.kg/mobilnye-telefony?page='
    pages = '?page='

    total_pages = get_total_pages(get_html(url))
    
    for page in range(1, total_pages+1):
        url_with_page = url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)
        

main()
