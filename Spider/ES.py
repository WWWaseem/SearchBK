# -*- coding: UTF-8 -*-
'''
@Author      ：WWW
@Date         ：2021/11/18 15:15
@Project    ：Test8_1.py
@File          ：ES.py


'''
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


# 创建索引
def create_index():
    mapping = {
        'properties': {
            'date': {
                'type': 'text'
            },
            'title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                "search_analyzer": "ik_smart"
            },
            'keywords': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                "search_analyzer": "ik_smart"
            },
            'des': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_smart'
            },
            'url': {
                'type': 'text'
            }
        }
    }
    # 判断索引是否存在
    if es.indices.exists(index='data') is not True:
        # 创建索引，指定索引名、索引·映射·
        res = es.indices.create(index='data', ignore=[400], body=mapping)
        print("无索引，创建它:\n", res)
    else:
        print("索引已经存在，跳过创建！")


# 删除索引
def delete_index(index):
    # 判断索引是否存在
    if es.indices.exists(index=index) is True:
        res = es.indices.delete(index=index, ignore=[400, 404])


def insertData(file):
    with open(file, mode='r', encoding='utf-8') as f:
        dicts = json.load(f)
        for dic in dicts:
            es.index(index='data', document=dic)


file = 'BK_50000.json'
# file = 'BK_30.json'
insertData(file)
