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
print("*"," "*14,"up主工具(评论用户抽奖系统)"," "*15,"*")
print("*"," "*7,"pc端打开用户主页,选择一条动态后点击转发按钮"," "*6,"*")
print("*"," "*7,"点击查看更多转发,将打开的页面网址复制到下方"," "*6,"*")
print("*"," "*56,"*")
print("*"*60)



url = input('请输入url')
forOidUrl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='
forUserUrl = 'https://api.bilibili.com/x/v2/reply'

header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
articleId = url[url.rindex('/')+1:url.index('?')]
print('已获取dynamic_id',articleId)

oidJson = json.loads(requests.get(forOidUrl + str(articleId)).content.decode('utf-8'))

oid1 = oidJson['data']['card']['desc']['rid']
oid2 = oidJson['data']['card']['desc']['dynamic_id']
print('oid1',oid1)
print('oid2',oid2)
type1 = 11
type11 = 1
# type17 = 17
tryParams = [str(oid1) + '-11', str(oid1) + '-1', str(oid1) + '-17', str(oid2) + '-11', str(oid2) + '-1', str(oid2) + '-17']
times = 0
flag = 1
userList = []
while flag:
    oid = tryParams[times].split('-')[0]
    type = tryParams[times].split('-')[1]
    print('oid',oid)
    print('type',type)
    try:
        forUserParamData1 = {'type':type,'sort':'2','oid':oid}
        print('forUserParamData1',forUserParamData1)
        for pn in range(1000000):
            forUserParamData1['pn'] = str(pn+1)
            userJson = json.loads(requests.get(forUserUrl,params = forUserParamData1,headers=header).content.decode('utf-8'))
            replies_ = userJson['data']['replies']
            if(replies_ == None):
                break
            respListSize = len(replies_)
            for index in replies_:
                userList.append({'uname':index['member']['uname'],'uid':index['member']['mid']})
        print("用户数据存储完毕")
        print("总评论用户数",len(userList))
        flag = 0
    except BaseException:
        times = times + 1
        if times == 6:
            print("程序错误")
            break
        print("发生异常")


print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','获取数据成功')
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','正在将数据写入文件,文件位置:F:/commentuser.txt')
allUser = open("F:/commentuser.txt","w")
allUser.truncate()
allUser.write('【总评论用户:】'+'\n')
for user in userList:
    allUser.write('用户名:'+str(user['uname'])+'  账号:'+str(user['uid'])+'\n')

print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','总评论人数:',len(userList))
print('【',time.strftime('%H:%M:%S',time.localtime(time.time())),'】','请输入需要抽取的人数')
luckNum= input()

allUser.write('【抽奖用户结果:】'+'\n')
for i in range(int(luckNum)):
    randomNum = random.randint(0,len(userList)-1)
    allUser.write('用户名:'+userList[randomNum]['uname']+' 账号:'+userList[randomNum]['uid']+'\n')
    print('随机选取结果==>',userList[randomNum]['uname'],'  ',userList[randomNum]['uid'])



