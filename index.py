from bs4 import BeautifulSoup
import os
import requests
import json
import re

def downLoadImg(imgSrc, downLoadPath):
    with open(downLoadPath, 'wb+') as file:
        imgRes = requests.get(imgSrc)
        file.write(imgRes.content)
        imgRes.close()

def getThreadList():
    threadList = []
    pageNo = 1
    while 1:    
        thredUrl = f'https://tieba.baidu.com/home/get/getthread?un=KOKOKOKOKO%E5%B7%A8%E8%9F%B9&pn={pageNo}&ie=utf8&_=1695037986699'
        res = requests.get(thredUrl)
        tr_list = json.loads(res.text)['data']['thread_list']
        tmpList = []
        for item in tr_list:
            title = item['title'].replace('/', '_')
            if len(re.findall('妖精尾巴|百年任務', title)) > 0:
                tmpList.append({'id': item['thread_id'], 'title': title})
        threadList.extend(tmpList)
        if len(tr_list) == 0:
            break
        pageNo += 1
    return threadList

def downLoadThreadList(id, title):
    if os.path.isdir(title):
        print('已存在，跳过下载')
        return
    print(f'开始下载:{title}')
    url = f'https://tieba.baidu.com/p/{id}?see_lz=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
    }
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    imgList = soup.find('div', id="j_p_postlist").findAll('img', {'class': 'BDE_Image'})

    if not os.path.exists(title) or not os.path.isdir(title):
        os.makedirs(title)

    i = 1
    for imgItem in imgList:
        downLoadImg(imgItem.get('src'), f'./{title}/{i}.jpg')
        i +=1
    res.close()
    print(f'下载成功：{title}')

for item in getThreadList():
    title = item['title']
    id = item['id']
    downLoadThreadList(id, title)

