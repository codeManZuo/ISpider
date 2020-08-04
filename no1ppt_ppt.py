import re

import requests
import pymysql
from bs4 import BeautifulSoup

header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
baseUrl = 'http://www.1ppt.com/moban/'
domain = 'http://www.1ppt.com'
typeUrlList = []

baseHtml = requests.get(baseUrl, headers=header).content.decode('gbk')
soup = BeautifulSoup(baseHtml, 'lxml')
typeEle = soup.find('div', class_='col_nav').find_all('a')
for ele in typeEle:
    typeInfo = {}
    typeInfo['name'] = ele.text
    typeInfo['url'] = ele['href']
    typeUrlList.append(typeInfo)
# print(typeUrlList)
typeUrlList = [{'name': '动态PPT模板', 'url': '/moban/dongtai/'}]

pptDetailList = []
for type in typeUrlList:
    typeBaseUrl = domain + type['url'] + 'ppt_' + (type['url'])[7:len(type['url']) - 1] + '_'
    for pn in range(1, 2):
        typeUrl = typeBaseUrl
        typeUrl = typeUrl + str(pn) + '.html'
        print('typeUrl',typeUrl)
        pptPageHtml = requests.get(typeUrl, headers=header).content.decode('gbk')
        soup = BeautifulSoup(pptPageHtml, 'lxml')
        ul = soup.find('ul', class_='tplist')
        allLi = ul.find_all('li')
        for li in allLi:
            pptDetail = {}
            pptDetail['firstImg'] = li.find('a').find('img')['src']
            pptDetail['pptName'] = li.find('a').find('img')['alt']
            currentDetailUrl = domain + li.find('a')['href']
            print('currentDetailUrl',currentDetailUrl)
            detailSoup = BeautifulSoup(requests.get(currentDetailUrl, headers=header).content.decode('gbk'), 'lxml')
            ulStr = str(detailSoup.find('div', class_='info_left').find('ul').text.replace('\n',''))
            pptDetail['type'] = re.findall('所属频道：([\\s\\S]*?)更新时间', ulStr, re.S)[0]
            allLi = detailSoup.find('div', class_='info_left').find('ul').find_all('li')
            allTagA = allLi[len(allLi)-1].find_all('a')
            tag = ''
            for t in allTagA:
                tag = tag + t.text + '#'
            pptDetail['tag'] = tag
            pptDetail['fileSize'] = re.findall('文件大小：([\\s\\S]*?)显示比例', ulStr, re.S)[0]
            pptDetail['note'] = re.findall('素材版本：([\\s\\S]*?)下载', ulStr, re.S)[0]
            pptDetail['onlinetime'] = re.findall('更新时间：([\\s\\S]*?)素材版本', ulStr, re.S)[0]
            pptDetail['detailInfo'] = detailSoup.find('div',class_='content').contents[0:1][0]
            pptDetail['spiderfrom'] = '第一ppt'
            pptDetail['downurl'] = detailSoup.find('ul',class_='downurllist').find('li').find('a')['href']
            pptDetailList.append(pptDetail)

print(pptDetailList)

# ppt模板名称1  代表预览图片1  预览图片详情1 所属类型1   标签1  大小1  介绍1   附加说明1  下载地址1  爬取来自1  上线时间1



