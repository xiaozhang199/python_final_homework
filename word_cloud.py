import sys
sys.path.append('d:\python\lib\site-packages')
from wordcloud import WordCloud
import jieba
from matplotlib import pyplot as plt#绘图，数据可视化
from PIL import Image#图片处理
import numpy as np#矩阵运算
import pymysql

link = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='zyx18080623585',
        database='crawldata',
        charset='utf8mb4')
cur = link.cursor()
sql = "SELECT title FROM up_infomation"
cur.execute(sql)  # 这里不是运行出来的文件，是运行的行数
data = cur.fetchall()
text = ""
for title in data:
    text += str(title[0])
cur.close()
link.close()

cut = jieba.cut(text)
string = ' '.join(cut)

img = Image.open(r'.\static\assets\images\cloud.jpg') #打开图片
img_array = np.array(img)#将图片转换为图片数组
wc = WordCloud(
        background_color = "white",
        mask = img_array,
        font_path = "STFANGSO.TTF"
)
wc.generate_from_text(string)

# #绘制图片
plt.imshow(wc)#其中wc为要处理的图像及数组，处理图像，对传入的数组或者图像进行处理并显示格式
plt.axis('off') #不显示坐标轴

# plt.show()#显示生成的词云图片
plt.savefig(r'.\static\assets\images\word.jpg',dpi = 800)#dpi是分辨率，默认分辨率有点低，要调高
