# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:46:40 2019

@author: luigi de lisi
"""
import re
import json
import datetime
from database import Db
import requests as r
from bs4 import BeautifulSoup as bs

def update_db(db, raw):
    c = get_conversion_values()
    soup = bs(raw, 'lxml')
    coin_table = soup.find('table', {'id' : 'currencies'})
    all_coins = coin_table.find_all('tr')
    info = get_info(all_coins)
    for i in info:
        db.add_to_table('data1', '(coin, name, market_cap, price, DailyVolume, circulating, DailyChange, logo, \
            WeeklyChange, currency, minable)', f'("{i[0]}", "{i[1]}", "{float(i[2])}", "{round(float(i[3]), 3)}", "{float(i[4])}", "{i[5]}", "{i[6]}", "{i[7]}", "{i[8]}", "USD", "{i[9]}")')
        db.add_to_table('data2', '(coin, name, market_cap, price, DailyVolume, circulating, DailyChange, logo, \
            WeeklyChange, currency, minable)', f'("{i[0]}", "{i[1]}", "{round(float(i[2])*c[0], 3)}", "{round(float(i[3])*c[0], 3)}", "{round(float(i[4])*c[0], 3)}", "{i[5]}", "{i[6]}", "{i[7]}", "{i[8]}", "EUR", "{i[9]}")')
        db.add_to_table('data3', '(coin, name, market_cap, price, DailyVolume, circulating, DailyChange, logo, \
            WeeklyChange, currency, minable)', f'("{i[0]}", "{i[1]}", "{round(float(i[2])*c[1], 3)}", "{round(float(i[3])*c[1], 3)}", "{round(float(i[4])*c[1], 3)}", "{i[5]}", "{i[6]}", "{i[7]}", "{i[8]}", "GBP", "{i[9]}")')

def get_info(table):
    for coin in table[1:]:
        symbol = coin.find('span', class_='currency-symbol')
        logo = coin.find('img', class_='logo-sprite')#['src']
        name = coin.find('a', class_='currency-name-container')#.text
        mrkt_cap = coin.find('td', class_='market-cap')#.text e da rimuovere \n
        price = coin.find('a', class_='price')#.text
        volume = coin.find('a', class_='volume')#.text
        circulating = coin.find('td', class_='circulating-supply')#.text da rimuovere \n e isolare codice moneta
        if '*' in circulating.text:
            minable = 0
        else:
            minable = 1
        change = coin.find('td', class_='percent-change')#.text
        week_graph = coin.find('img', class_='sparkline')#['src']
        yield symbol.text, name.text, re.sub("\W","",mrkt_cap.text), re.sub(r'[^\w.]', '',price.text), re.sub("\W","",volume.text), re.sub('[^0-9]','', circulating.text), change.text, logo['src'], week_graph['src'], minable

def get_conversion_values():
    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    req = r.get(url)
    d = json.loads(req.text)
    eur = d['rates'].get('EUR')
    gbp = d['rates'].get('GBP')
    return eur, gbp

if __name__ == '__main__':
    d = Db('crypto.db')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    url = 'https://coinmarketcap.com'
    req = r.get(url, headers=headers)
    if d.is_empty():
        statement = '("coin" TEXT UNIQUE, "name" TEXT UNIQUE, "market_cap" REAL, "price" REAL, \
            "DailyVolume" REAL, "circulating" INTEGER, "DailyChange" TEXT, "logo" TEXT, "WeeklyChange" TEXT, "currency" TEXT, "minable" INTEGER)'
        d.new_table('data1', statement)
        d.new_table('data2', statement)
        d.new_table('data3', statement)
    else:
        pass
    if req.status_code == 200:
        update_db(db=d, raw=req.text)
    else:
        now = datetime.datetime.now() 
        with open('log.txt', 'w') as f:
            f.write(f'\nURL ERROR {req.status_code} [{now.strftime("%d/%m/%Y %H:%M:%S")}]')





