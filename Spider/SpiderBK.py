# -*- coding: UTF-8 -*-
'''
@Author      ：WWW
@Date         ：2021/11/17 14:00
@Project    ：Test8_1.py 
@File          ：Spider.py


'''
import time
import urllib
import requests
import re
import os
import shutil
import html
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


def get_info(url):
    """
    获取编码信息
    获取title
    获取content
    获取url
    list_page : 已经爬取
    count : 计数
    list_urlFind : 找到的url
    """
    # global , list_page, count, symbol
    global count, list_data, list_page, list_url, seed_net
    # 避免重复爬取

    # START 获取编码格式charset
    try:
        response = requests.get(url=url, headers=header)
        curUrl = response.url
        if curUrl in list_page:
            return
        if curUrl[-1] == '/':
            curUrl = curUrl[:-1]
        response.encoding = re.findall(r'charset=(.+?)"', response.text)[0].replace('\'', '').replace('\"', '')
        htmlText = html.unescape(response.text)
    except:
        # print('charset  ' + url)
        list_url.pop(0)
        return

    bsObj = BeautifulSoup(htmlText, 'lxml')
    # 提取a标签的url
    list_a = bsObj.find_all('a')
    list_urlFind = []
    for i in list_a:
        list_urlFind.append(i.get('href'))
    list_urlFind = list(filter(None, list_urlFind))
    # 写入数据
    try:
        for i in list_urlFind:
            if i[0:10] == 'javascript' or i[0] == '#' or i in list_url:
                continue
            i = urljoin(curUrl, i)
            netloc = urllib.parse.urlparse(i).netloc
            query = urllib.parse.urlparse(i).query
            if (len(list_url) < 50000 and netloc == seed_net and query != 'force=1') and (i not in list_url and i not in list_page):
                list_url.append(i)
                # print(i)
    except:
        return

    try:
        title = bsObj.title.string.split('_')[0]
        if title in list_title:
            raise IndexError
        new_data = {
            "date": bsObj.find(attrs={"itemprop": "dateUpdate"})['content'],
            'title': bsObj.title.string.split('_')[0],
            'keywords': bsObj.find(attrs={"name": "keywords"})['content'],
            'des': bsObj.find(attrs={"name": "description"})['content'],
            'url': curUrl
        }
        list_data.append(new_data)
        count += 1
        print(str(count) + ' ' + curUrl)
        list_page.append(curUrl)
        list_title.append(title)
    except:
        print('WastePage  ' + curUrl + '  list_url : ' + str(len(list_url)))
        list_url.pop(0)
        return

    # 记录当前值


count = 0
list_data = []
list_firUrl = []
list_secUrl = []
list_page = []
list_title = []
list_url = []
seed_net = ''
if __name__ == "__main__":
    # Step 0 : 指定文件
    targetNum = 1
    file = 'BK_' + str(targetNum) + '.json'
    if os.path.exists(file):
        os.remove(file)
    # Step 1 : 指定url
    seed = 'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%E4%B8%8E%E6%8A%80%E6%9C%AF/663582'
    seed_net = urllib.parse.urlparse(seed).netloc
    list_url.append(seed)
    # Step 2 : 进行UA伪装
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
    }
    while len(list_page) < targetNum and len(list_url) != 0:
        url = list_url[0]
        list_url.pop(0)
        get_info(url)
        time.sleep(0.3)
    with open(file, mode='a+', encoding='utf-8') as f:
        json.dump(list_data, f)
