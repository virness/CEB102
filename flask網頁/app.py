import pymongo
import plotly as py
from flask import Flask, render_template
from flask import Flask,request,redirect,url_for,session

# 雲端連線，也可本機連線  帳號:密碼 @ 資料庫網址
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster0.pl1kjxk.mongodb.net/?retryWrites=true&w=majority")
#選擇資料庫 創建 Shopping然後建立用戶users欄位
db = client.shopping
collection=db.users
# #定義flask 公開 預設/
app=Flask(__name__,static_folder="static",static_url_path="/")
# #建立session的key
app.secret_key='try it myfirst and you'

@app.route("/")  #由於前面已經先預設了這個可略過
def index():
    return render_template('index.html')

#註冊頁面
@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

#顯示頁面
@app.route("/show", methods=['POST'])
def show():
    name=request.values["name"]
    password=request.values["password"]
    email=request.values["email"]
    phone=request.values["phone"]
    birthday=request.values["birthday"]
    addr=request.values["addr"]     
    result=collection.find_one({"email":email})
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")

    data=collection.insert_one({"name":name,"password":password,"email":email,"phone":phone,"birthday":birthday,"addr":addr})

    return render_template('show.html',**locals())
        
#登入頁面 成功進入member.html 失敗則導向error.html
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#登入後則可選修改資料，登出
@app.route("/member", methods=['POST'])
def member():
    email=request.values["email"]
    password=request.values["password"]
    result=collection.find_one({"$and":[{"email":email},{"password":password}]})

    if result ==None:
        return render_template("login.html",msgs="帳號或密碼輸入錯誤")

    session['name']=result['name']
    name=result['name']
    email=result['email']
    phone=result['phone']
    birthday=result['birthday']
    addr=result['addr']
    return render_template('member.html',**locals())

        
# 讓網址後面變成 /error?msg=錯誤訊息
@app.route("/error")
def error():
    message=request.args.get("msg","")
    return render_template('error.html',message=message)  

@app.route("/signout")
def signout():
    del session['name']
    return redirect("/")
@app.route("/pm25")
def pm25():
    return render_template('pm25.html')
@app.route("/pm225")
def pm225():
    return render_template('pm225.html')
@app.route("/water")
def water():
    return render_template('water.html')
@app.route("/weather")  
def weather():
    return render_template('weather.html')
@app.route("/weathers")  
def weathers():
    return render_template('weathers.html')


#下方就是直接讀取所有app的裝飾器 並且run全部
if __name__ == '__main__':
    app.run(port=8999)
    