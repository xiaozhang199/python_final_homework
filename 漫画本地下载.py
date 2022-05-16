import re #正则表达式的提取
from urllib.request import urlretrieve  # 将远程数据传入本地的库函数
from bs4 import BeautifulSoup #亮汤提取
import requests #提取网页的源代码
import os #文件下载时的路径处理
import lxml #亮汤提取为'lxml'文件，这种文件的容错性更强
from tqdm import tqdm #这个是显示进度的函数，有了这个，就可以实时看到文件下载到本地的进度
from contextlib import closing #管理类上文管理的关闭功能，实例化，运行完成后，会调用类的close方法。
import time #暂停多少秒后继续执行

def main():
    dir_path = create_file() #创建保存文件的路径
    urllist,url_name = get_url() #得到每一个章节的链接和名字
    down_file(urllist,url_name,dir_path) #根据章链接，名字和路径下载每一张图片

def create_file():
    dir_name = "镖人"
    if dir_name not in os.listdir(r"D:\python\finalProject"):
        os.mkdir(dir_name)
    string = "D:\\python\\finalProject\\"+dir_name
    return string

def get_url():
    target_url = "https://www.dmzj.com/info/biaoren.html"
    info = requests.get(target_url)#得到镖人漫画首页的源代码
    bs = BeautifulSoup(info.text, 'lxml')#beautifulsoup提取元素
    main_part = bs.find('ul', class_='list_con_li')
    comic_con_li = main_part.find_all('a')#找到所有漫画标题和链接的位置
    section_list = []
    section_title = []
    for section in comic_con_li:
        section_list.insert(0, section['href'])
        section_title.insert(0, section.text)
    return  section_list,section_title

def down_file(url_list,url_name,file_path):
    for i,url in enumerate(tqdm(url_list)):#tqdm展示下载的进度表
        name = url_name[i]
        #创建当前漫画章节名的文件夹
        create_section_path = os.path.join(file_path,name)
        if name not in os.listdir(file_path):
            os.mkdir(create_section_path) #创建每个章节的名字
        info = requests.get(url=url,timeout=20)
        bs = BeautifulSoup(info.text, 'lxml') #得到每个章节内部的信息
        # 得到我们需要的动态加载的数据：script-->因为是内部加载，所以可以找出来
        graph_info = str(bs.script)
        page_pre = re.findall('\|(\d{4})\|', graph_info)[0]
        page_next = re.findall('\|(\d{5,6})\|', graph_info)[0] #第二季目录可能存在5个或6个数字
        # 图片具体数字有13位或者14位
        # 注意：13位的数字改成14位后还要复原，否则链接无法点入
        pages = re.findall('\|(\d{13,14})\|', graph_info)
        for index in range(len(pages)):
            if len(pages[index]) == 13:
                pages[index] += '0'
        #漫画图片的顺序由小到大逐渐排序
        pages.sort(key=lambda x: int(x))
        pagelist = []
        base_url = "https://images.dmzj.com/img/chapterpic/"
        for page in pages:
            if str(page)[-1] == '0':
                page = page[:13]
            page_url = base_url + str(page_pre) + "/" + str(page_next) + "/" + str(page) + ".jpg"
            pagelist.append(page_url)

        head = {
            "Referer":url
        }#此处是因为你必须从前一个链接点入

        for index,page in enumerate(pagelist):
            page_name = '%03d.jpg'%(index + 1)
            page_save_path = os.path.join(create_section_path, page_name)
            #一种良好的文件管理，接收和自动关闭流
            with closing(requests.get(page, headers=head, stream=True)) as response:#stream 参数设置为True，推迟下载响应内容直到访问Response.content属性
                chunk_size = 1024 #chunk_size:设置逐次迭代的数据大小
                if response.status_code == 200:
                    with open(page_save_path, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):#iter_content:逐次输出，防止一次性撑爆内存
                            file.write(data)
                else:
                    print('无法正确写入图片')
        time.sleep(2)#爬一个章节，休息两秒，不要给对方服务器太大压力

if __name__ == "__main__":
    main()
