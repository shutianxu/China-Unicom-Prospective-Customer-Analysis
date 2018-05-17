# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:34:37 2017

@author: 1707501
"""

'''
crawler car dealer information
'''

import requests
from bs4 import BeautifulSoup
import json
import re
# http://dealer.bitauto.com/beijing/

# http://dealer.bitauto.com/beijing/audi/?BizModes=0&page=1

# get pages info
def get_infos(soup):    
    pageinfo = soup.find_all('div',class_='pagination')
    pageinfo = pageinfo[0].find_all(href=re.compile("page"))
    pages = []
    for page in pageinfo:
        if page['href'] not in pages:
            pages.append(page['href'])
    return pages

# parse 4s_name/brand/add/district info
def parse_name_add_dis(dealers):
    tels = ""
    for dealer in dealers:
        try:
            stor_name = dealer.find_all('div',class_='col-xs-6 left')[0].h6.a.get_text()
            brand = dealer.find_all('p',class_='brand')[0].get_text()
            add = dealer.find_all('div',class_='col-xs-6 left')[0].find_all('p',class_='add')[0].span.next_sibling['title']
            district = dealer.find_all('div','col-xs-7 middle')[0].p.get_text()
#<span class="tel400atr" id="100124507" dealerid="100124507">400-813-2251</span>
            tel = dealer.find_all('span','tel400atr')[0]['dealerid']
            tels += tel + ','
            line = stor_name +'\t'+ brand +'\t'+ district +'\t'+ add + '\t'+ tel + '\n'
            print(line)
            with open(r'E:\documents\work\work\20171117\dealer7.txt','a',encoding='utf-8') as f:
                f.write(line)
        except:
            print('pases error!')
    return tels

# get telephone infomation
def get_tel(telephones):
    url_get_tel_first = "http://autocall.bitauto.com/eil/das2.ashx?userid="
    url_get_tel_second = "&mediaid=10&source=bitauto"
    url_get_tel = url_get_tel_first + telephones + url_get_tel_second
    print(url_get_tel)
    try:
        get_tel = requests.get(url_get_tel,headers=headers)
        tel_str = get_tel.text[18:-1]
        tel_list = json.loads(tel_str)
        for tel in tel_list:
            line = tel["dealerId"] +'\t'+ tel["tel"] + '\n'
            print(line)
            with open(r'E:\documents\work\work\20171117\dealer7_tel.txt','a',encoding='utf-8') as f:
                f.write(line)
    except:
        print("paser tel error!")



headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }

province = ["beijing","shanghai","tianjin","chongqing","shandong","jiangsu","zhejiang","guangdong","hebei","henan","sichuan","hunan","shaanxi","liaoning","anhui","fujian","shanxi","hubei","yunnan","neimenggu","jiangxi","heilongjiang","jl","guangxi","guizhou","xinjiang","gansu","ningxia","qinghai","hainan","xizang"]

province_small = ["beijing","shanghai","tianjin"]

brand_List = ["audi","alfaromeo","astonmartin","alpina","arcfox-289","bj","bmw","mercedesbenz","honda","peugeot","buick","bydauto","porsche","borgward","besturn","bisuqiche-263","daoda-282","beiqihuansu","shenbao","ww","beijingjeep","beiqixinnengyuan","bjqc","bentley","bugatti","barbus","cajc","casyc","changanqingxingche-281","changankuayue-283","greatwall","changheauto","changjiangev","chenggong","volkswagen","dongfengfengdu","dongfengfengguang","fs","fengxingauto","dongfengxiaokang-205","dongfeng-27","southeastautomobile","dodge","ds","toyota","ford","fiat","ferrari","feichishangwuche","foday","fujianxinlongmaqichegufenyouxiangongsi","foton","faradayfuture","gq","gonow","qorosauto","sinogold","gmc-109","hafu-196","hama","hanteng","faw-hongqi","huataiautomobile","hafeiautomobile","higer","chtc","huakai","sgautomotive","huasong","shanghaihuizhong-45","geely","jac","jauger","jeep","jmc","jinbei","kinglongmotor","jlkc","joylongautomobile","gwev","traumcadil","lackaiyi","chrysler","karry","lexus","renult","lynkco","lincoln","landwind","landrover","lifanmotors","suzuki","rolls-royce","lamborghini","cf","everus","ludifangzhou","mazda","mg-79","mini","mclaren","maserati","luxgen","acura","pagani","chery","venucia","kia","chautotechnology","singulato","isuzu","nissan","roewe","skoda","subaru","smart","siwei","saleen","mitsubishi","maxus","sam","ssangyong","tesla","denza","techart","sgmw","volvo","wey","weilaiqiche","isuzu-132","eurise","enranger","chevrolet","citroen","hyundai","xingchi","infiniti","yusheng-258","ym","faw","zotyeauto","brillianceauto","zhidou","zhinuo","zxauto"]

brand_List_small = ["audi","alfaromeo"]

url_first_field = 'http://dealer.bitauto.com'

# iteration crawler 
for city in province_small:
    for br in brand_List_small:
        url = url_first_field + '/' + city + '/' + br + '/'
        print(url)
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'html5lib')
        dealers = soup.find_all('div',class_="row dealer-list")
        tels = parse_name_add_dis(dealers)
        get_tel(tels)
        try:
            webpages = get_infos(soup)
        except:
            continue
        print(webpages)
        for page in webpages:
            web_url = 'http://dealer.bitauto.com' + page
            print(web_url)
            response = requests.get(web_url,headers=headers)
            soup = BeautifulSoup(response.text,'html5lib')
            dealers = soup.find_all('div',class_="row dealer-list")
            pagetels = parse_name_add_dis(dealers)
            get_tel(pagetels)
# dealers = soup.find_all('div',class_="row dealer-list")



        