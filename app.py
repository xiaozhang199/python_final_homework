from flask import Flask
from flask import render_template
import jinja2
import pymysql
import sys
sys.path.append('d:\python\lib\site-packages')
from wordcloud import WordCloud
import jieba
from matplotlib import pyplot as plt#绘图，数据可视化
from PIL import Image#图片处理
import numpy as np#矩阵运算

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/list")
def movie():
    datalist = []
    link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='**********',
        database='crawldata',
        charset='utf8mb4')
    cur = link.cursor()
    sql = "select * from up_infomation"
    cur.execute(sql)  # 这里不是运行出来的文件，是运行的行数
    data = cur.fetchall()
    for item in data:
        datalist.append(list(item))
    cur.close()
    link.close()
    return render_template("list.html", videos=datalist)

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")


@app.route('/comment')
def comment():
    datalist = []
    link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='********',
        database='crawldata',
        charset='utf8mb4')
    cur = link.cursor()
    sql = "SELECT COUNT(*) FROM up_infomation WHERE comment_num < 1000"
    cur.execute(sql)  
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE comment_num between 1000 and 10000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE comment_num between 10000 and 100000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE comment_num >= 100000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    cur.close()
    link.close()
    return render_template("comment.html",datalist=datalist)


@app.route('/view')
def view():
    datalist = []
    link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='*********',
        database='crawldata',
        charset='utf8mb4')
    cur = link.cursor()
    sql = "SELECT COUNT(*) FROM up_infomation WHERE view_num < 100000"
    cur.execute(sql)  
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE view_num between 100000 and 300000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE view_num between 300000 and 500000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE view_num between 500000 and 1000000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    sql = "SELECT COUNT(*) FROM up_infomation WHERE view_num > 1000000"
    cur.execute(sql)
    data = cur.fetchall()
    for nums in data:
        for num in nums:
            datalist.append(num)
    cur.close()
    link.close()
    return render_template("view.html",datalist=datalist)

@app.route('/share')
def share():
    datalist = []
    link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='********',
        database='crawldata',
        charset='utf8mb4')
    cur = link.cursor()
    sql = "select * from up_infomation ORDER BY share_num DESC LIMIT 10"
    cur.execute(sql)  
    data = cur.fetchall()
    for item in data:
        datalist.append(list(item))
    cur.close()
    link.close()
    return render_template("list.html", videos=datalist)

@app.route('/word')
def word():
    return render_template("word.html")

if __name__ == '__main__':
    app.run()
