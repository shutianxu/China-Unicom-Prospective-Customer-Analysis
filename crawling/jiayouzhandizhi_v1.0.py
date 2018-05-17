# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 11:06:48 2018

@author: 1707500
"""
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json


def get_one_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    try:
        response = requests.get(url,headers = headers)                  
        if response.status_code == 200:                     #判断是否爬取网页成功
            return response.text
        return None
    except RequestException:
        return None
    
    
def parse_page(html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('ul li p')

            a=[]
            for l in lls:
                a.append(l.get_text().strip())
                
            return a
        except:
            pass    
        
        
def write_to_file(content):
    with open('D:\document\crawling\shanghaijiayouzhan.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)  +'\n')
        f.close()



data = []
for i in range(30):
    print(i)
    url = 'https://energy.cngold.org/jyzwd_4_587_p'+ str(i+1) +'.htm'
    html = get_one_page(url)
    df = parse_page(html)    
    data = data + df
print(data)
write_to_file(data)

