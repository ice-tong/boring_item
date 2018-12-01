# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:24:47 2018

@author: icetong
"""

import requests
from urllib.parse import quote
import time

key_word = "iphone"
page_num = 10

url = "https://ai.taobao.com/search/getItem.htm"

parmas = {'_tb_token_': '353a8b5a1b773', '__ajax__': '1', 
          'pid': 'mm_10011550_0_0', 'page': '1', 'pageSize': '60', 
          'sourceId': 'search', 'pageNav': 'false',
          'key': quote(key_word), 'debug': 'false', 'maxPageSize': '200',
          'npx': '50'}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
           /537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

result = []
for p in range(1, page_num+1):
    parmas['page'] = str(p)
    r = requests.get(url, headers=headers, params=parmas)
    data = r.json()
    items = data['result']['auction']
    for item in items:
        desc = item['description']
        itemId = str(item['itemId'])
        location = item['itemLocation']
        nick = item['nick']
        picUrl = item['picUrl']
        price = str(item['price']) if 'price' in item else '--'
        realPrice = str(item['realPrice'])
        saleCount = str(item['saleCount'])
        result.append([itemId, desc, nick, location, price, 
                       realPrice, saleCount, picUrl])
    print("page: {}".format(p))
    time.sleep(2)

with open("{}.csv".format(key_word), "w", encoding="gbk") as f:
    f.write(",".join(['itemId', 'desc', 'nick', 'location', 'price', 
                       'realPrice', 'saleCount', 'picUrl'])+'\n')
    content = "\n".join([",".join(l) for l in result])
    f.write(content.encode("gbk", "ignore").decode("gbk"))