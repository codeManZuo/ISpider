import re
import pymysql
import requests
from bs4 import BeautifulSoup

baseUrl = 'https://www.jqhtml.com/down/category/resources/java/page/'
header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "referer": "https://www.jqhtml.com/",
}

detailUrlList = []
fileNameList = []
allTagList = []
panUrlList = []
panCodeList = []
# content-list-item
for pn in range(50,77):  #rang(x,y) 从第x+1页到第y页
    currentPageUrl = baseUrl + str(pn+1)
    print('当前请求页'+currentPageUrl)
    pageHtml = requests.get(currentPageUrl, headers=header).content.decode('utf-8')
    soup = BeautifulSoup(pageHtml, 'lxml')
    pageEleList = soup.find_all('div', class_='content-list-item')
    for ele in pageEleList:
        aTemp = ele.find('a')
        detailUrlList.append(aTemp['href'])
        fileNameList.append(aTemp.text)

# print(detailUrlList)

for detailUrl in detailUrlList:
    detaiResp = requests.get(detailUrl, headers=header).content.decode('utf-8')
    detailSoup = BeautifulSoup(detaiResp, 'lxml')
    tagList = detailSoup.find('div', class_='single-tags').find_all('a')
    tagTxt = ''
    for tag in tagList:
        tagTxt = tagTxt + "#" + tag.text
    # print(tagTxt)
    allTagList.append(tagTxt)
    a = detailSoup.find('div',class_='alert-down')
    panUrlList.append(re.findall('a class="pan" href="([\\s\\S]*?)" target="_blank"', str(a), re.S)[0])
    panCodeList.append(re.findall('密码:<span>([\\s\\S]*?)</span></div>', str(a), re.S)[0])
    print('已抓取...')

# print(panUrlList)
# print(len(panUrlList))
# print(panCodeList)
# print(len(panCodeList))
# print(fileNameList)
# print(len(fileNameList))
# print(allTagList)
# print(len(allTagList))
conn = pymysql.connect(host="localhost", user="root", passwd="1020", db='ziyuan', charset='utf8', port=3306)
cursor = conn.cursor()
insert_sql = "insert into zy_pdf_bddisk(url,code,name,tag) values (%s,%s,%s,%s);"
#返回受影响的行数

for i in range(len(panUrlList)):
    row1 = cursor.execute(insert_sql,(panUrlList[i], panCodeList[i], fileNameList[i], allTagList[i]))
    print('已存储第',i,'行数据')

conn.commit()
cursor.close()
conn.close()

# java pdf系列