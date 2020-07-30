
import re

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
panUrlList = []
panCodeList = []
# content-list-item
for pn in range(1):
    currentPageUrl = baseUrl + str(pn+1)
    print('当前请求页'+currentPageUrl)
    pageHtml = requests.get(currentPageUrl, headers=header).content.decode('utf-8')
    soup = BeautifulSoup(pageHtml, 'lxml')
    pageEleList = soup.find_all('div', class_='content-list-item')
    for ele in pageEleList:
        aTemp = ele.find('a')
        detailUrlList.append(aTemp['href'])
        fileNameList.append(aTemp.text)

print(detailUrlList)

for detailUrl in detailUrlList:
    detaiResp = requests.get(detailUrl, headers=header).content.decode('utf-8')
    detailSoup = BeautifulSoup(detaiResp, 'lxml')
    a = detailSoup.find('div',class_='alert-down')
    panUrlList.append(re.findall('a class="pan" href="([\\s\\S]*?)" target="_blank"', str(a), re.S)[0])
    panCodeList.append(re.findall('密码:<span>([\\s\\S]*?)</span></div>', str(a), re.S)[0])

print(panUrlList)
print(panCodeList)
print(fileNameList)




