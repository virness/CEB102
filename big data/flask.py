#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pymongo import MongoClient
# from bson.objectid import ObjectId
import pandas as pd
conn = MongoClient(host=['localhost:27017'])
db = conn.testDB
collection = db.testCollection
df=pd.read_csv('test.csv')
records = df.to_dict('records') # 參數 record 代表把列轉成個別物件
collection.insert_many(records)


# In[ ]:

from flask import Flask
from flask import request
import pymongo
import pandas as pd
from pymongo import MongoClient
from flask import render_template
app = Flask(__name__)
@app.route("/post", methods=['GET', 'POST'])
def submit():
    conn = MongoClient(host=['localhost:27017'])
    db = conn.testDB
    collection = db.testCollection
    cursor = collection.find({})
    df=pd.DataFrame(list(cursor))
    del df['_id']
    if request.method == 'POST':
        keyword = request.values['username']
        df = df[(df['股票代號'] == int(keyword) )]
        return render_template("post.html",tables=[df.to_html(classes='data', header="true", index = False)])
    else:
        return render_template("post.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0")






#<img src="{{ url_for('static', filename='2330.jpg') }}" width="800" height="600" />

