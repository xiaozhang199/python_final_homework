import requests
import json
from lxml import etree
import time
import pymysql

def get_data():
    space_url = 'https://space.bilibili.com/473837611'#个人空间链接-->新华社的数据
    search_url = 'https://api.bilibili.com/x/space/arc/search'#我们搜索时展现的信息链接
    mid = space_url.split('/')[-1]#个人空间标志

    #requests库的session对象能够帮我们跨请求保持某些参数，也会在同一个session实例发出的所有请求之间保持cookies。
    sess = requests.Session()
    search_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*'}#头文件参数尽可能多写
    ps = 30
    datalist = []
    for pn in range(1, 11):
        search_params = {'mid': mid,
                         'ps': ps,
                         'tid': 0,
                         'pn': pn}
        req = sess.get(url=search_url, headers=search_headers, params=search_params, verify=False)
        info = json.loads(req.text)#b站的数据是用json形式存储的
        vlist = info['data']['list']['vlist']
        for video in vlist:
            data = []
            title = video['title']
            data.append(title)#添加标题
            bvid = video['bvid']
            video_url = 'https://www.bilibili.com/video/' + bvid  # 具体视频连接
            data.append(video_url)
            comment = video['comment']#评论数量
            data.append(comment)
            view_num = video['play']#观看数量
            data.append(view_num)
            time.sleep(1)#及时休眠，不要给对方服务器太大压力
            video_response = sess.get(url=video_url, headers=search_headers, verify=False).content#lxml文件更容错性更高
            selector = etree.HTML(video_response)#通过xpath找出每个要提取的信息
            coin_span = selector.xpath("//span[@class='coin']")
            coin_num = coin_span[0].xpath("text()")[0].strip(' ').strip('\n').strip(' ')  # 硬币数量
            data.append(coin_num)
            dm_span = selector.xpath("//span[@class='dm']")
            dm_num = dm_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 弹幕数量
            data.append(dm_num)
            like_span = selector.xpath("//span[@class='like']")
            like_num = like_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 喜欢数量
            data.append(like_num)
            share_span = selector.xpath("//span[@class='share']")
            share_num = share_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 分享数量
            data.append(share_num)
            collect_span = selector.xpath("//span[@class='collect']")
            collect_num = collect_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 收藏数量
            data.append(collect_num)
            datalist.append(data)
    return datalist

def init_db():
    #2.连接mysql客户端
    link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='zyx18080623585',
        database='crawldata',
        charset='utf8mb4')

    # 3.创建游标对象
    cur = link.cursor()

    try:
        sql = "CREATE TABLE if NOT EXISTS up_infomation( " \
              " id INT PRIMARY KEY auto_increment," \
              " title VARCHAR(200)," \
              " link VARCHAR(200)," \
              " comment_num int," \
              " view_num int," \
              " coin_num int," \
              " dm_num VARCHAR(200)," \
              " like_num VARCHAR(200)," \
              " share_num int," \
              " collect_num int)"

        cur.execute(sql)

        # 提交到数据库-->查询不需要提交
        link.commit()
    except Exception as error:
        print(error)
        # 数据回滚
        link.rollback()
    finally:
        # 6.关闭游标
        cur.close()
        # 7.关闭连接
        link.close()

def savedata(datalist):
    init_db()
    link = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='zyx18080623585',
            database='crawldata',
            charset='utf8mb4')
    cur = link.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 8 or index == 6 or index == 7:
                if(data[index][-1] == '万'):
                    data[index] = int(float((data[index][:-1]))*10000)
                else:
                    data[index] = int(data[index])
        sql = '''
                insert into up_infomation (
                title,link,comment_num,view_num,coin_num,dm_num,like_num,share_num,collect_num)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, data)
        link.commit()
    cur.close()
    link.close()

if __name__ == "__main__":
    data = get_data()
    savedata(data)
