# @author: 程序员大晖
# @date: 2020/7/20

import requests
import json
import random
import time
logo = '''  
 ___     ___     _       ___     ___     ___     _       ___
| _ )   |_ _|   | |     |_ _|   | _ )   |_ _|   | |     |_ _| 
| _ \    | |    | |__    | |    | _ \    | |    | |__    | |   
|___/   |___|   |____|  |___|   |___/   |___|   |____|  |___| 
'''

print("*"*60)
print(logo)
print("*"," "*56,"*")
print("*"," "*14,"up主工具(转发用户抽奖系统)"," "*15,"*")
print("*"," "*7,"pc端打开用户主页,选择一条动态后点击转发按钮"," "*6,"*")
print("*"," "*7,"点击查看更多转发,将打开的页面网址复制到下方"," "*6,"*")
print("*"," "*56,"*")
print("*"*60)


forUserUrl = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id='
offset = ''
header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','请输入网址:')
url = input()
articleId = url[url.rindex('/')+1:url.index('?')]
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','获取动态id成功:',articleId)

hasMore = True
# 存储用户信息
userListResult = []
total = 0
userJson = ''
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','正在获取转发用户...')
while hasMore:
    forUserUrl = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id='+str(articleId)+'&offset='
    forUserUrl = forUserUrl+offset
    userJson = json.loads(requests.get(forUserUrl,headers=header).content.decode('utf-8'))
    userList = userJson['data']['items']
    for user in userList:
        id = user['desc']['user_profile']['info']['uid']
        name = user['desc']['user_profile']['info']['uname']
        userListResult.append({'uname':name,'uid':id})

    if(int(userJson['data']['has_more']) == 1):
        hasMore = True
        offset = userJson['data']['offset']
    else:
        hasMore = False

total = userJson['data']['total']
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','获取数据成功')
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','正在将数据写入文件')
allUser = open("F:/forwarduser.txt","w")
allUser.truncate()
allUser.write('【总用户信息:】'+'\n')
for user in userListResult:
    allUser.write('用户名:'+str(user['uname'])+'  账号:'+str(user['uid'])+'\n')
allUser.write('\n')

print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','总转发人数:',total)
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','请输入需要抽取的人数')

luckNum= input()

allUser.write('【抽奖用户结果:】'+'\n')
for i in range(int(luckNum)):
    randomNum = random.randint(0,len(userListResult)-1)
    allUser.write('用户名:'+str(user['uname'])+'  账号:'+str(user['uid'])+'\n')
    print('随机选取结果==>',userListResult[randomNum]['uname'],'  ',userListResult[randomNum]['uid'])