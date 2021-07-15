from newspaper import Article
import nltk
import xlrd
import requests  #爬取网页的库
import re
from urllib import parse
from bs4 import BeautifulSoup #用于解析网页的库
import time
import sys
import urllib.request

# 构造请求头
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }


# 选择数据源
read_path="陕西源-编辑.xlsx"
bk = xlrd.open_workbook(read_path)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("榕整体陕西源汇总")
except:
    print("no sheet in %s named sheet1" % read_path)


# 判断二级链接是否具有域名，没有的话需要拼接
def ifHasNetloc(url,link):
    linkTest = parse.urlparse(link)
    if (linkTest.netloc != ""):
        return link
    else:
        my_url = parse.urlparse(url)
        # print(my_url)
        naninani = my_url.scheme + '://' + my_url.netloc
        naninani = naninani + link
        if(my_url.netloc in naninani):
            # print(naninani)
            return naninani

# 读取基本信息
def getBaseInfo(url):
    name = sh.cell_value(i, 1)  # 读取公告名称
    print(name + ":" + url)
    shengfen = sh.cell_value(i, 3)  # 读取省份
    dishi = sh.cell_value(i, 4)  # 读取地市
    print(dishi + dishi)
    print('=' * 40)


def checjlink(hosturl,url):
    # 输入网址

    html_doc = url
    if len(sys.argv) > 1:
        website = sys.argv[1]
        if (website is not None):
            html_doc = sys.argv[1]
    # 获取请求
    req = urllib.request.Request(html_doc)
    # 打开页面
    webpage = urllib.request.urlopen(req)
    # 读取页面内容
    html = webpage.read()
    # 解析成文档对象
    soup = BeautifulSoup(html, 'html.parser')  # 文档对象
    # 非法URL 1
    invalidLink1 = '#'
    # 非法URL 2
    invalidLink2 = 'javascript:void(0)'
    # 集合
    result = set()
    # 计数器
    mycount = 0
    # 查找文档中所有a标签

    for k in soup.find_all('a'):
        # print(k)
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link == invalidLink1:
                pass
            elif link == invalidLink2:
                pass
            elif link.find("javascript:") != -1:
                pass
            else:
                mycount = mycount + 1
                # print(mycount,link)
                result.add(link)
        # print("打印超链接个数:",mycount)
        # print("打印超链接列表",result)
    f = open(r'result.text', 'w', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
    for a in result:
        f.write(a + "\n")
    f.close()
    print("\r\n扫描结果已写入到result.text文件中\r\n")

# 二级链接依次访问
def childPass(url):
    print('3、关键字所在的a href标签提取:' + url)
    response = requests.request("GET", url, headers=headers)  # 获取网页数据
    response.encoding = response.apparent_encoding  # 当获取的网页有乱码时加
    soup = BeautifulSoup(response.text, 'html.parser')
    bf = soup.find('div', class_='view TRS_UEDITOR trs_paper_default trs_web')

    # 提取关键字
    linklst = []
    for x in soup.find_all('a', href=re.compile('html')):
        link = x.get('href')
        if("logout" in link):
            return
        if("login" in link):
            return
        if ("void" in link):
            return
        if ("user" in link):
            return
        if("javascript" in link):
            return
        if link:
            linklst.append(link)
            if(ifHasNetloc(url, link)):
                naninani = ifHasNetloc(url, link)
                checkifContainUrl(naninani)

# 获取页面的li中a的值
def get_title_html(html_1):   #
    soup=BeautifulSoup(html_1,"html.parser")
    title_url_Date=soup.find('div',class_='clearfix dirconone').find_all('li')
    for i in title_url_Date:
        # print(i)
        url=i.find('a')['href']
        # print(url)


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
            return
        a.parse()
        if(a.title):
            print('标题 : ' + a.title +'         链接==' + url)
            zhaopinresult = "招聘" in a.title
            if zhaopinresult:
                print('存在招聘信息的标题::' + a.title + '         链接== ' + url)
                print(a.text)
                f = open(r'result.text', 'w', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
                f.write(url + "\n")
                f.close()
                print("\r\n扫描结果已写入到result.text文件中\r\n")

# 获取总行数
nrows = sh.nrows
print('=' * 40)
print("1、数据源的个数=",nrows)

for i in range(nrows):
    url = sh.cell_value(i,11)  # 依次读取每行第11列的数据，也就是 URL
    print("2、访问第%d个链接:",i + 1)
    print('=' * 40)
    getBaseInfo(url)
    childPass(url)
    # checjlink(url)
    print('=' * 40)
