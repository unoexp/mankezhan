import requests
import json
import os
import re

from picmix import *

if not os.path.exists('dl'):
    os.mkdir('dl')


# ==========账号密码===========
acc = 'your_account'
pswd = 'your_password'
# ==========账号密码===========


    
# ==========登录部分===========
login_url = 'https://member.mkzcdn.com/login/account/'

data = {
    'account' : acc,
    'password' : pswd
}
# 登录 获得sign
res = requests.post(login_url, data)
if not '登录成功' in res.text:
    exit('登录失败')

sign = json.loads(res.text)['data']['sign']
uid = json.loads(res.text)['data']['uid']
print(sign)

# 获得cookies
cookie = {
    '__login_his_sync': '0',
    'tourist_expires': '1',
    'redirect_url': 'https://www.mkzhan.com/user/',
    'LOGINSIGN': '59910867' + ':' + sign,
    'HISTORYPS': '1',
    '__login_account': acc
}
# ==========登录部分===========


# ==========爬虫部分===========
# 获得人气排行榜
res = requests.get('https://www.mkzhan.com/top/popularity/', cookies=cookie)
# 正则搜索所有漫画id
# "/\d+/"
res = list(set(re.findall('"/\d+/"', res.text)))


for m_id in res:
    # 获得漫画id
    m_id = m_id.replace('"', '')
    m_id = m_id.replace('/', '')

    listurl='https://comic.mkzcdn.com/chapter/?comic_id=' + m_id
    infourl='https://comic.mkzcdn.com/comic/info/?comic_id=' + m_id
    # 下载漫画章节名
    info=requests.get(infourl, cookies=cookie).text
    # 去除章节信息里的非法字符
    name=re.sub('[\/:*?"<>|]','',json.loads(str(info))['data']['title'])
    print('\n正在开始爬取' + name)
    # 下载漫画章节链接
    listinfo=requests.get(listurl, cookies=cookie).text
    c=json.loads(listinfo)['data']
    
    # 创建漫画目录
    if not os.path.exists(name): 
        os.mkdir(name+'/')

    # 为测试方便只遍历前5章
    debug = 5

    # 遍历每一章
    for n in c:
        page = 0
        chap = re.sub('[\/:*?"<>|]','',n['title']) # 标题用来作为文件夹名
        chap_id = n['chapter_id'] # id用来拼接url
        path = name + '/' + chap + '/'
        # 章节是否存在
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print('('+str(round(c.index(n)/(len(c)-1)*100,1))+'%) '+chap+' 已存在')
            continue
        
        url = 'https://comic.mkzcdn.com/chapter/content/v1/' 
        # 下载此章包含的图片url
        param = {
            'chapter_id': chap_id,
            'comic_id': m_id,
            'format': '1',
            'quality': '1',
            'sign': sign,
            'type': '1',
            'uid': uid
        }
        a = json.loads(requests.get(url, params=param, cookies=cookie).text)
        a = a['data']['page']
        for m in a:
            url=m['image']
            dl=requests.get(url, cookies=cookie).content\
            # 保存图片
            open(path + str(page) + '.jpg', 'wb+').write(dl)
            page += 1
        print('('+str(round(c.index(n)/(len(c)-1)*100,1))+'%) '+chap+' 已下载')

        debug -= 1
        if debug == 0:
            break
    print(name + '已爬取完毕, 正在处理图片')
    picmix(name)
    
# ==========爬虫部分===========


