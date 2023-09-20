import requests
from bs4 import BeautifulSoup
import os
import json


class IP_Poor:
    proxyUrlList = []
    def __init__(self):
        pass
    def check(self, url, targetUrl='https://www.baidu.com'):
        proxies = {
            'http': url,
            'https': url
        }
        try:
            requests.get(targetUrl, proxies = proxies)
        except:
            return False
        return True
    def __getProxyData(): 
        res = []
        url = f'https://www.docip.net/data/free.json'
        response = requests.get(url)
        data = json.loads(response.text)
        for item in data['data']:
            pStr = 's' if item['proxy_type'] == '1' else ''
            url = item['ip']
            res.extend(f'http{pStr}://{url}')
        return res
    def save(self):
        urlList = self.__getProxyData()
        with open('./IP_Poor.txt', 'w+', encoding='utf-8') as file:
            for url in urlList:
                isOk = self.check(url)
                print(f"{url}  {'成功' if isOk else '失败'}")
                if isOk:
                    self.proxyUrlList.extend(url)
                    file.write(f'{url}\n')


if __name__ == '__main__':
    ip_poor = IP_Poor()
    print(ip_poor.proxyUrlList)