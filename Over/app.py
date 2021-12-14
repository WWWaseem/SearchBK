import re

import jieba
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request


def getStopwords(url):
    with open(url, encoding='utf-8') as fp:
        temp = fp.read()
    fp.close()
    return set(temp.split('\n'))


def getCut(text, stopwords):
    data = jieba.cut(text)
    target_word = [x for x in data if x not in stopwords]
    return list(target_word)


def getIndexEnd(string, pattern):
    starts = [each.start() for each in re.finditer(pattern, string)]
    ends = [start + len(pattern) - 1 for start in starts]
    wordsRange = [[start, end] for start, end in zip(starts, ends)]
    DOWN = sorted(wordsRange, key=lambda x: x[1], reverse=True)
    return DOWN


def highlight(string, pattern):
    for i in pattern:
        index = getIndexEnd(string, i)
        for j in index:
            des = list(string)
            des.insert(int(j[1]) + 1, "</font>")
            des.insert(int(j[0]), "<font color='red'>")
            string = ''.join(des)
    return string


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__)


@app.route('/')
def loadStr():
    return render_template("index.html")


# Step 1 : 通过GET/POST获取查询词
@app.route("/<keyword>", methods=["GET", "POST"])
def getStr(keyword):
    global stopwords
    if request.method == 'POST':
        keyword = request.form["keyword"]
    else:
        keyword = keyword
    keyword = keyword.strip()
    if len(keyword) == 0:
        return render_template("index.html")
    words = getCut(keyword, stopwords)
    print(words)

    # Step 2 : 设置每个属性的权重比例, 搜索ElasticSearch数据库
    query = {
        "bool": {
            "should": [
                {"match": {
                    "title": {
                        "query": keyword,
                        "boost": 2
                    }
                }},
                {"match": {
                    "keywords": {
                        "query": keyword,
                        "boost": 5
                    }
                }},
                {"match": {
                    "des": {
                        "query": keyword,
                        "boost": 3
                    }
                }}
            ]
        }
    }

    result = es.search(index='data', query=query)['hits']['hits']
    list_res = []
    for res in result:
        # Step 3 : 对数据进行渲染
        res['_source']['des'] = highlight(res['_source']['des'], words)
        res['_source']['keywords'] = highlight(res['_source']['keywords'], words).split(',')
        # for i in res['_source']['keywords']:
        #     print(i)
        list_res.append(res['_source'])

    return render_template("response.html", keyword=keyword, list_res=list_res, len=len(list_res))


if __name__ == '__main__':
    stopwords = getStopwords('cn_stopwords.txt')
    app.run(debug=True, port=3600)
