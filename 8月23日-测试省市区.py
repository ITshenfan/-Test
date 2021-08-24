import cpca
import newspaper.article
from cpca import drawer
from newspaper import Article
import folium

location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "北京朝阳区北苑华贸城", "北京市朝阳区南湖渠","河南省新乡市延津县"]
url = 'http://edu.sc.gov.cn/scedu/c100495/2021/5/26/dea2af6a21a54f4e8e616c4172136559.shtml'
a = Article(url, language='zh')






print('cpca.transform_text_with_addrs解析')
text = '你好呀'
try:
    df2 = cpca.transform_text_with_addrs(text)
    print('解析成功')
except:
    print('解析失败')






a.download()
a.parse()
print(a.text)
print('cpca.transform_text_with_addrs解析')
# df2 = cpca.transform_text_with_addrs(a.text)
print('cpca.transform_text_with_addrs解析成功')
province = df2['省'].get(0)
city = df2['市'].get(0)
qu = df2['区'].get(0)




print(province)
print(city)
print(qu)




# 标注到地图上
# drawer.draw_locations(df[cpca._ADCODE], "df.html")


