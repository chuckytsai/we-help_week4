# 載入模組
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from markupsafe import escape
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
import os
import json

# 建立Application物件
# 設定靜態檔案的路徑處理
app = Flask(
    __name__,
    static_folder="material",  # 靜態檔案的資料匣名稱
    static_url_path="/Alice"
)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 建立首頁
@app.route("/")
def index():
    return render_template("index.html")

def find_name():
    # 讀取帳號密碼Json檔案
    with open(r"material/vip/np.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

# 宣告變數為使用者輸入的帳號密碼
    inputNameValue=request.values.get("whatName")
    inputPWValue=request.values.get("whatPW")
    flag = False

# 找出是否有帳號密碼在vip.json中
    for psycho in range(0, len(data["nightwalker"])):
        if data["nightwalker"][psycho]["name"] == inputNameValue and data["nightwalker"][psycho]["password"] == inputPWValue:
            inputName = inputNameValue
            inputPW = inputPWValue
            session["whatName"]=inputName
            flag=True
            break
    if flag:
        return inputName,inputPW
    else:
        return "getout","getout"

# 建立登入頁面並且判斷帳號密碼登入通往其他頁面(POST)
@app.route("/signin", methods=["POST"])
def signin():
    name ,password= find_name()
    if password=="getout":
        return redirect("/error")
    if name=="getout":
        return redirect("/memberName")
    else:
        return redirect(url_for("member"))

# 登入成功頁面(session)
@app.route("/member")
def member():
    if "whatName" in session:
        return render_template("member.html")
    else:
        return redirect("/")

# 登入(帳號成功密碼錯誤)
@app.route("/memberName")
def memberName():
    return render_template("memberName.html")

# 帳號密碼皆錯
@app.route("/error")
def error():
    return render_template("error.html")

# 登出帳號且瀏覽器忘記該帳號訊息
@app.route('/logout')
def logout():
    session.pop("whatName", None)
    return redirect(url_for('index'))

# 用port3000
app.run(port=3000)
