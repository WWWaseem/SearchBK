# -*- coding: UTF-8 -*-
'''
@Author      ：WWW
@Date         ：2021/11/19 9:52 
@Project    ：Test8_1.py 
@File          ：search.py


'''
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# query = {
#     'match': {
#         'keywords': '计算机',
#         # 'search_analyzer': 'ik_smart'
#     }
# }
keywords = '李白的诗句'
query = {
    "bool": {
        "should": [
            {"match": {
                "title": {
                    "query": keywords,
                    "boost": 5
                }
            }},
            {"match": {
                "keywords": {
                    "query": keywords,
                    "boost": 3
                }
            }},
            {"match": {
                "des": {
                    "query": keywords,
                    "boost": 2
                }
            }}
        ]
    }
}
result = es.search(index='data', query=query)['hits']['hits']
for res in result:
    print(res['_source'])
    print(res['_source']['keywords'].split(', '))
