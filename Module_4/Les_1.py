# pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import pandas
import sqlite_client


links_to_parse = [
    'https://www.kufar.by/l/mebel',
    'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MiwicGl0IjoiMjg0MjQ1MDAifQ%3D%3D&elementType=popular_categories',
    'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MywicGl0IjoiMjg0MjQ1NTcifQ%3D%3D&elementType=popular_categories,'
    'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6NCwicGl0IjoiMjg0MjQ1NTcifQ%3D%3D&elementType=popular_categories'

]
def get_mebel_by_link(link):
    response = requests.get(link)
    mebel_data = response.text

    mebel_items = []
    to_parse = BeautifulSoup(mebel_data, 'html.parser')
    for elem in to_parse.find_all('a', class_='styles_wrapper__5FoK7'):
        try:
            price, decription = elem.text.split('р.')
            mebel_items.append((
                elem['href'],
                int(price.replace(' ', '')),
                decription
            ))
        except:
            print(f'Цена не была указана. {elem.text}')

    return mebel_items


def save_to_csv(mebel_items):
    pandas.DataFrame(mebel_items).to_csv('mebel.csv', index=False)


def save_to_sqlite(mebel_items):
    connection = sqlite_client.get_connection()
    for item in mebel_items:
        sqlite_client.insert(connection, item[0], item[1], item[2])


def run():
    mebel_items = []
    for link in links_to_parse:
        mebel_items.extend(get_mebel_by_link(link))
    save_to_sqlite(mebel_items)


run()
