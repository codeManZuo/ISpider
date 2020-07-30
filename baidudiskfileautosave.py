'''
1.获取到网盘链接和提取码
2.第一个请求是(get)到网盘提供的资源链接,这一步需要获取到请求时cookie中的BDCLND,这个值是下一步请求中一个参数logid的计算入参
3.第二个请求是(post)到verify地址,这个请求是携带上了提取码,验证的步骤,这个请求会返回一个randsk参数,这个参数需要放入cookie中的BDCLND(更新),作为下一次请求的认证,表示已经经过提取码验证
4.第三个请求是请求第一次的网盘链接地址,这个时候我们已经让cookie中携带了本次提取码的验证成功的cookie,所以可以直接进入到资源展示界面
5.第四个请求是保存文件
    - 保存文件需要注意一下几个问题:
        1).fsidlist,shareid,from这三个参数是变化的,获取的方式是从第三个请求的响应中通过正则截取一个json串,然后获取
        2).保存时需要有用户登录认证信息,程序暂时没有做自动登录获取认证信息的功能(因为baidudisk网页版登录绝大部分第一次登录都需要短信验证码,这样爬虫程序也是会有交互操作),这里
        你需要在浏览器登录好将任意请求的cookie中的认证信息的两个参数存入cookie中,这两个参数如下:
                    (1).STOKEN
                    (2).BDUSS
'''
import json
import time
import re
import requests
import execjs

class Pan():

    def __init__(self,session,logid1):
        logo = '''  
   ___              _        _             ___      _              _     
  | _ )   __ _     (_)    __| |   _  _    |   \    (_)     ___    | |__  
  | _ \  / _` |    | |   / _` |  | +| |   | |) |   | |    (_-<    | / /  
  |___/  \__,_|   _|_|_  \__,_|   \_,_|   |___/   _|_|_   /__/_   |_\_\  

'''
        print("*"*80)
        print(logo)
        print(" "*18,"百度网盘自动存储脚本"," "*17,)
        print("*"*80)

        self.session = session
        self.logid1 = logid1
        self.userId = input('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'请输入网盘账号')
        self.usersite = 0;
        tokenFile = open('./panbaidu/token.txt')
        tokenList = tokenFile.readlines()

        for index,ele in enumerate(tokenList):
            if (index+1)%3 == 1:
                if(ele[0:len(ele)-1].__eq__(self.userId)):
                    self.usersite = index
                    break

        self.stoken = tokenList[self.usersite+1][0:len(tokenList[self.usersite+1])-1]
        self.bduss = tokenList[self.usersite+2][0:len(tokenList[self.usersite+2])-1]

        self.savePath = input('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'请输入存储位置路径')
        self.panUrl = input('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'请输入网盘资源链接')
        self.panCode = input('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'请输入网盘资源提取码')


    def writeLog(self,msg):
        logFile = open('./panbaidu/pan.log', 'a')
        logFile.write('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+msg+'\n')
        logFile.close()

    # 第一次访问网盘资源的外链,目的是获取cookie中的BDCLND,从而生成logid,进而可以进行verify的请求,拿到randsk,更新BDCLND来请求资源外链获取资源展示页面
    def getFristCookie(self):
        bdUrl = 'https://pan.baidu.com/s/1k75vMOQjzVKSWi1BEzIutw'
        header = {
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        self.session = requests.Session()
        self.session.get(bdUrl,headers=header)
        e = self.session.cookies.get_dict().get('BAIDUID')
        print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'第一次获取BDCLND成功:'+e)
        return e

    # 生成logid
    def get_logid(self,bid):
        with open('./panbaidu/w.js', encoding='utf-8') as f:
            jsfile = f.read()
        js = execjs.compile(jsfile)
        logid = js.call('getLogId', bid)
        print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'调用js文件生成logid'+logid)
        return logid

    def get1(self):
        cookie = self.getFristCookie()
        logid = self.get_logid(cookie)
        self.logid1 = logid
        return logid

    # 组装第一次请求(verify)的url
    def get_url_get_file_with_code(self):
        urlSplitTemp = self.panUrl.split('/')
        temp_ = urlSplitTemp[len(urlSplitTemp) - 1]
        getUrl = 'https://pan.baidu.com/share/verify?surl=' + temp_[1:len(temp_)] + '&t=' + str(time.time()*1000).split('.')[0] +'&channel=chunlei&web=1&app_id=250528&bdstoken=6316be392358cf57ec4ffa5ca96bb371&logid=' + str(self.get1()) + '&clienttype=0'
        print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'已生成本次verify请求的url和date并写入日志')
        self.writeLog('verify请求路径:'+getUrl)
        return getUrl

    # 发送verify请求
    def get_file_with_code(self):
        header = {
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://pan.baidu.com/",
        }
        getUrl = self.get_url_get_file_with_code()
        params = {
            'pwd': self.panCode,
            'vscode': '',
            'vscode_str': '',
        }
        resp = json.loads(requests.post(getUrl,headers=header, data=params).text)
        print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'verify请求已发送')
        return resp


# 保存资源
pan = Pan('','')
resp1 = pan.get_file_with_code()
header = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://pan.baidu.com/",
}
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'第二次获取BDCLND成功:'+resp1['randsk'])
c = requests.cookies.RequestsCookieJar()
c.set("BDCLND", resp1['randsk'])
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'已更新cookie中的BDCLND')
pan.session.cookies.update(c)
resp = pan.session.get(pan.panUrl, headers=header).content.decode('utf-8')
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'已获取网盘资源')
dataJson = re.findall('yunData.setData\(([\\s\\S]*?)\);', resp, re.S)[0]

dataJson = json.loads(dataJson)
# 接下来就是保存文件到网盘中
fsidlist = dataJson['file_list']['list'][0]['fs_id']
fromId = dataJson['uk']
shareId = dataJson['shareid']

channel = 'chunlei'
web = '1'
app_id = 250528
bdstoken = '6316be392358cf57ec4ffa5ca96bb371'

urlSave = 'https://pan.baidu.com/share/transfer?shareid='+str(shareId)+'&from='+str(fromId)+'&channel=chunlei&web=1&app_id=250528&bdstoken='+bdstoken+'&logid='+pan.logid1+'&clienttype=0'
pan.session.cookies.set('STOKEN',pan.stoken,domain=".baidu.com")
pan.session.cookies.set('BDUSS',pan.bduss,domain=".baidu.com")
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'已生成本次保存资源的请求url和data并写入日志')
saveData = {
            'fsidlist': '['+str(fsidlist)+']',
            'path': pan.savePath,
        }
pan.writeLog('本次保存资源的请求url和data'+urlSave+'  '+str(saveData))
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'资源保存中...')
respSave = pan.session.post(urlSave, headers=header,data=saveData).content.decode('utf-8')
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'保存成功,位置如下:')
print(json.loads(respSave)['extra']['list'][0]['to'])
print('【'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'】'+'欢迎下次使用   @author: blog.onsee.vip  程序员大晖')



