from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__)


@app.route('/')
def loadStr():
    return render_template("index.html")


@app.route("/<keyword>", methods=["GET", "POST"])
def getStr(keyword):
    if request.method == 'POST':
        keyword = request.form["keyword"]
    else:
        keyword = keyword
    keyword = keyword.strip()
    if len(keyword) == 0:
        return render_template("index.html")
    query = {
        "bool": {
            "should": [
                {"match": {
                    "title": {
                        "query": keyword,
                        "boost": 5
                    }
                }},
                {"match": {
                    "keywords": {
                        "query": keyword,
                        "boost": 3
                    }
                }},
                {"match": {
                    "des": {
                        "query": keyword,
                        "boost": 2
                    }
                }}
            ]
        }
    }

    result = es.search(index='data', query=query)['hits']['hits']
    list_res = []
    for res in result:
        list_key = res['_source']['keywords'].split(',')
        res['_source']['keywords'] = list_key
        list_res.append(res['_source'])
    return render_template("response.html", keyword=keyword, list_res=list_res, len=len(list_res))


# @app.route("/getStr/<str>", methods=["GET", "POST"])
# def clickStr():
#     keyword = request.form["keyword"]
#     query = {
#         'match': {
#             'des': keyword
#         }
#     }


if __name__ == '__main__':
    # run()
    app.run(debug=True)
