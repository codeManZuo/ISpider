import time

import requests
from bs4 import BeautifulSoup
import urllib
import os


baseUrl1 = 'https://www.easyicon.net/iconsearch/'
baseUrl2 = '/?m=yes&f=_all&s=addtime_DESC'
baseUrl3 = 'https://www.easyicon.net'
detailUrlList = []
header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

currentPage = 1
key = input('请输入搜索关键词')
os.mkdir('D:/myfile/模板网站积累/资源/spiderfiletemp/' + key)

firstReqHtml = requests.get(baseUrl1 + key + '/' + str(currentPage) + baseUrl2, headers=header).content.decode('utf-8')
soup = BeautifulSoup(firstReqHtml, 'lxml')
pageEle = soup.find('div', class_='pages_all')
allPages = 1
allFindEle = pageEle.find_all('a')
if len(allFindEle) == 0:
    allPages = 1
else:
    allPages = allFindEle[len(allFindEle) - 1].string

print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','已获取总页数:',allPages)

# 页数
for pg in range(int(allPages)):
    url1 = ''
    url1 = baseUrl1 + key + '/' + str(pg+1) + baseUrl2
    firstReqHtml = requests.get(baseUrl1 + key + '/' + str(currentPage) + baseUrl2, headers=header).content.decode('utf-8')
    soup = BeautifulSoup(firstReqHtml, 'lxml')
    detailEleList = soup.find('ol').find_all('div',class_='icon_img')
    for u in detailEleList:
        detailUrlList.append(baseUrl3+u.find('a')['href'])

print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','已获取所有连接:',detailUrlList)


for u in detailUrlList:
    firstReqHtml = requests.get(u, headers=header).content.decode('utf-8')
    soup = BeautifulSoup(firstReqHtml, 'lxml')
    iconEleList = soup.find(class_='sub_img_box').find_all('td')
    del(iconEleList[-1])
    # 遍历每一个td标签
    for i in iconEleList:
        src =i.find('img')['src']
        alt = i.find('img')['alt']
        urllib.request.urlretrieve(baseUrl3 + src, 'D:/myfile/模板网站积累/资源/spiderfiletemp/' + key + '/' + alt[0:len(alt) - 5] + '_' + str(detailUrlList.index(u)) + '.png')