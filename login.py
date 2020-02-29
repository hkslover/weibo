import requests
import execjs
import time
import re
session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
def login(nonce,prelt,pcid,sp,su,rsakv):
    header = {'Host': 'login.sina.com.cn',
    'Origin': 'https://weibo.com',
    'Referer': 'https://weibo.com/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    url1 = 'https://login.sina.com.cn/cgi/pin.php?&s=0&p=' + pcid
    response = session.get(url1,headers = headers)
    with open('door.png','wb') as f:
        f.write(response.content)
    door = input("请输入验证码:")
    data =  {'entry': 'weibo',
            'gateway': 1,
            'from': '',
            'savestate': 0,
            'qrcode_flag': 'false',
            'useticket': 1,
            'pagerefer': '',
            'vsnf': 1,
            'door': door,
            'su': su,
            'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1',
            'service': 'miniblog',
            'servertime': int(round(time.time())),
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1536*864',
            'encoding': 'UTF-8',
            'prelt': prelt,
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'}
    response = session.post(url,headers = header,data = data)
    response.encoding = 'gbk'
    return response.text
def get_sp(me,pwd):
    with open('wb.js','r') as f:
        js_code = f.read()
    sp = execjs.compile(js_code).call('get_sp',me,pwd)
    return sp
def get_me(su):
    params = {'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': su,
            'rsakt': 'mod',
            'checkpin': 1,
            'client': 'ssologin.js(v1.4.19)',
            '_':int(round(time.time() * 1000))}
    url = 'https://login.sina.com.cn/sso/prelogin.php'
    response = session.get(url,headers = headers,params = params)
    #print(response.text)
    return response.text.replace('sinaSSOController.preloginCallBack','')
def get_su(user):
    with open('wb.js','r') as f:
        js_code = f.read()
    su = execjs.compile(js_code).call('get_su',user)
    return su
su = get_su('账号')
me = get_me(su)
nonce = eval(me).get('nonce')
pcid = eval(me).get('pcid')
prelt = eval(me).get('exectime')
rsakv = eval(me).get('rsakv')
#print(nonce)
sp = get_sp(eval(me),"密码")
print(login(nonce,prelt,pcid,sp,su,rsakv))
