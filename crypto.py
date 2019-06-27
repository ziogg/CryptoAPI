# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:46:40 2019

@author: luigi de lisi
"""
import re
import datetime
from database import Db
import requests as r
from bs4 import BeautifulSoup as bs

d = Db('crypto.db')

def update_db():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    url = 'https://coinmarketcap.com'
    req = r.get(url, headers=headers)   
    if req.status_code == 200:
        raw = req.text
        soup = bs(raw, 'lxml')
        d.new_table('data', '("coin" TEXT UNIQUE, "name" TEXT UNIQUE, "market_cap" REAL, "price_USD" REAL, "DailyVolume" REAL, "circulating" REAL, "DailyChange" TEXT, "logo" TEXT, "WeeklyChange" TEXT)')
        coin_table = soup.find('table', {'id' : 'currencies'})
        all_coins = coin_table.find_all('tr')
        info = get_info(all_coins)
        for i in info:
            d.add_to_table('data', '(coin, name, market_cap, price_USD, DailyVolume, circulating, DailyChange, logo, WeeklyChange)', f'("{i[0]}", "{i[1]}", "{float(i[2])}", "{round(float(i[3]), 3)}", "{float(i[4])}", "{i[5]}", "{i[6]}", "{i[7]}", "{i[8]}")')
    else:
        now = datetime.datetime.now() 
        with open('log.txt', 'w') as f:
            f.write(f'\nURL ERROR {req.status_code} [{now.strftime("%d/%m/%Y %H:%M:%S")}]')

def get_info(table):
    for coin in table[1:]:
        symbol = coin.find('span', class_='currency-symbol')
        logo = coin.find('img', class_='logo-sprite')#['src']
        name = coin.find('a', class_='currency-name-container')#.text
        mrkt_cap = coin.find('td', class_='market-cap')#.text e da rimuovere \n
        price = coin.find('a', class_='price')#.text
        volume = coin.find('a', class_='volume')#.text
        circulating = coin.find('td', class_='circulating-supply')#.text da rimuovere \n e isolare codice moneta
        change = coin.find('td', class_='percent-change')#.text
        week_graph = coin.find('img', class_='sparkline')#['src']
        yield symbol.text, name.text, re.sub("\W","",mrkt_cap.text), re.sub("\W","",price.text), re.sub("\W","",volume.text), re.sub('[^0-9]','', circulating.text), change.text, logo['src'], week_graph['src']


if __name__ == '__main__':
    update_db()