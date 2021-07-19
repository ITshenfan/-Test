from newspaper import Article
import nltk
import xlrd
import requests  #爬取网页的库
import re
from urllib import parse
from bs4 import BeautifulSoup #用于解析网页的库
import time
import pymysql

# 构造请求头
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }


# 选择数据源
read_path= "../测试/陕西源-编辑.xlsx"
bk = xlrd.open_workbook(read_path)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("榕整体陕西源汇总")
except:
    print("no sheet in %s named sheet1" % read_path)



# 读取基本信息
def getBaseInfo(url):
    name = sh.cell_value(i, 1)  # 读取公告名称
    print(name + ":" + url)
    shengfen = sh.cell_value(i, 3)  # 读取省份
    dishi = sh.cell_value(i, 4)  # 读取地市
    print(dishi + dishi)
    print('=' * 40)

# 判断二级链接是否具有域名，没有的话需要拼接,返回二级的http链接
def GetSecondLinkHasNetloc(firstlink,link):
    linkTest = parse.urlparse(link)
    if (linkTest.netloc != ""):
        return link
    else:
        my_url = parse.urlparse(firstlink)
        naninani = my_url.scheme + '://' + my_url.netloc
        naninani = naninani + link
        if(my_url.netloc in naninani):
            return naninani


# 二级链接是否是有效的招聘公告
def secondaryLinkValid(secondaryLink):
    if ("logout" in secondaryLink):
        return "123"
    if ("login" in secondaryLink):
        return "123"
    if ("void" in secondaryLink):
        return "123"
    if ("user" in secondaryLink):
        return "123"
    if ("javascript" in secondaryLink):
        return "123"



# 得到a标签下的二级链接
def getSecondUtl(firsturl):
    response = requests.request("GET", firsturl, headers=headers)  # 获取网页数据
    response.encoding = response.apparent_encoding  # 当获取的网页有乱码时加
    soup = BeautifulSoup(response.text, 'html.parser')
    bf = soup.find('div', class_='view TRS_UEDITOR trs_paper_default trs_web')

    # 提取二级链接的地址
    linklst = []
    # for x in soup.find_all('a', href=re.compile('html')):
    for x in soup.find_all('a'):
        link = x.get('href')
        if link:
            if ("logout" in link):
                return
            linklst.append(link)
            if(GetSecondLinkHasNetloc(firsturl, link)):
                naninani = GetSecondLinkHasNetloc(firsturl, link)
                if(secondaryLinkValid(naninani) != "123"):# 如果二级链接有效，再判断是否有标题和正文
                    checkifContainUrl(naninani)




# 获取页面的li中a的值
def get_title_html(firsturl):
    response = requests.request("GET", firsturl, headers=headers)  # 获取网页数据
    response.encoding = response.apparent_encoding  # 当获取的网页有乱码时加
    soup = BeautifulSoup(response.text, 'html.parser')
    bf = soup.find('div', class_='view TRS_UEDITOR trs_paper_default trs_web')

    # 提取二级链接的地址
    linklst = []
    # for x in soup.find_all('a', href=re.compile('html')):
    for x in soup.find_all('a'):

        link = x.get('href')
        if ("logout" in link):
            continue
        if ("login" in link):
            continue
        if ("void" in link):
            continue
        if ("user" in link):
            continue
        if ("javascript" in link):
            continue
        if link:
            linklst.append(link)
            if (GetSecondLinkHasNetloc(firsturl, link)):
                naninani = GetSecondLinkHasNetloc(firsturl, link)
            else:
                continue

    soup=BeautifulSoup(naninani,"html.parser")
    title_url=soup.find('div',class_='clearfix dirconone').find_all('li')
    for i in title_url:
        url=i.find('a')['href']
        if (GetSecondLinkHasNetloc(firsturl, link)):
            naninani = GetSecondLinkHasNetloc(firsturl, link)
            if (secondaryLinkValid(naninani) != ""):  # 如果二级链接有效，再判断四否有标题和正文
                checkifContainUrl(naninani)

# 判断标题是否存在"招聘"，如果有，提取正文
def checkifContainUrl(url):
    try:
        response = requests.request("GET", url, headers=headers)  # 获取网页数据
    except:
        print("服务器拒绝连接........")
        print("让我休息5秒钟啊！！！")
        print("ZZzzzz...")
        time.sleep(5)
        print("做了个美美的梦，睡的很好, 那我们继续吧...")
        return
    response.encoding = response.apparent_encoding  # 当获取的网页有乱码时加
    soup2 = BeautifulSoup(response.text, 'html.parser')
    bf = soup2.find('div', class_='view TRS_UEDITOR trs_paper_default trs_web')
    a = Article(url, language='zh')
    if(a):
        a.download()
        if(a.download_exception_msg):
            print("出现网页下载异常：",a.download_exception_msg)
            return
        a.parse()
        if(a.title):
            if("无障碍" in a.title):
                return
            print('标题 : ' + a.title +'         链接==' + url)
            # scrip = open(r'爬取过程中涉及到的链接.txt', 'a+', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
            # scrip.write(url + "\n" + a.title + "\n")
            # scrip.close()

            zhaopinresult = "招聘" in a.title
            if zhaopinresult:
                print('存在招聘信息的标题::' + a.title + '         链接== ' + url)
                print(a.text)
                # f = open(r'resultDicTest/%s.txt'%a.title, 'w', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
                # f.write(url + "\n" + a.title + "\n"  + "\n" + "\n"+ a.text + "\n")
                # f.close()
                # print("\r\n扫描结果已写入到result.text文件中\r\n")
                db = pymysql.connect(host='127.0.0.1',
                                     port=3306,
                                     user='root',
                                     password='12345678',
                                     db="shanxiyuan",
                                     charset='utf8'
                                     )  # 连接数据库
                cursor = db.cursor()
                sql = "INSERT INTO EMPLOYER(LINK,TITLE,TEXT) VALUES (%s, %s,  %s)" % (a.title, url, a.text)
                try:
                    cursor.execute(sql)
                    db.commit()
                    print('插入数据成功')
                except:
                    db.rollback()
                    print("插入数据失败")
                db.close()


def create():
    db = pymysql.connect(host='127.0.0.1',
                         port=3306,
                         user='root',
                         password='12345678',
                         db="shanxiyuan",
                         charset='utf8'
                         )  # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS EMPLOYER")

    sql = """CREATE TABLE MAINTEXT (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            LINK  CHAR(255),
            TITLE CHAR(20),
            TEXT CHAR(255) )"""

    cursor.execute(sql)
    db.close()


def insert(value):
    db = pymysql.connect(host='127.0.0.1',
                         port=3306,
                         user='root',
                         password='12345678',
                         db="shanxiyuan",
                         charset='utf8'
                         )  # 连接数据库
    cursor = db.cursor()
    sql = "INSERT INTO EMPLOYER(LINK,TITLE,TEXT) VALUES (%s, %s,  %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


# 获取总行数
nrows = sh.nrows
print('=' * 40)
print("1、数据源的个数=",nrows)
create()

for i in range(nrows):
    url = sh.cell_value(i,11)  # 依次读取每行第11列的数据，也就是 URL
    print("2、访问第%d个链接:"%i + 1)
    getBaseInfo(url)
    getSecondUtl(url)
    print('=' * 40)

