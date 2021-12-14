# -*- coding: UTF-8 -*-
'''
@Author      ：WWW
@Date         ：2021/11/18 15:15
@Project    ：Test8_1.py
@File          ：ES.py


'''
import json
from elasticsearch import Elasticsearch

# Step 1 : 连接Elastic Search
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def create_index():
    # Step 2 : 设置映射(数据处理规则)
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
    """
    date：
    链接网页更新时间，以text格式存储。
    title：
    词条标题，以text格式存储。依据ik_max_word模式进行倒排索引建立，依据ik_smart模式进行词条检索。
    keywords：
    词条关键词，以text格式存储。依据ik_max_word模式进行倒排索引建立，依据ik_smart模式进行词条检索。
    des：
    词条描述，以text格式存储。依据ik_max_word模式进行倒排索引建立，依据ik_smart模式进行词条检索。
    url：
    链接网页URL，以text格式存储。
    """
    # Step 3 : 根据映射创建索引
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

# Step 4 : 插入数据
def insertData(file):
    with open(file, mode='r', encoding='utf-8') as f:
        dicts = json.load(f)
        for dic in dicts:
            es.index(index='data', document=dic)


file = 'BK_50000.json'
# file = 'BK_30.json'
insertData(file)
