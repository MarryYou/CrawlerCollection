from bs4 import BeautifulSoup
import requests
import json
import time
from random import choice
from database import DataBase
import pymongo


class CeawlInit:
    # 初始化一些需要的东西
    # 搜狗微信文章下列表的baseurl 以及 列表下几个分类的url
    # 注:网页的第一次显示数据以及后续加载的文章请求地址是不同的
    def __init__(self):
        self.base_url = 'http://weixin.sogou.com/pcindex/pc/'
        self.new_list = []
        for i in range(0, 21):
            self.new_list.append(self.base_url + 'pc_' +
                                 str(i)+'/pc_'+str(i)+'.html')
        # 这里是首页第一次返回的列表中url
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        ]
        # 利用random的包来随机返回use-agent 因为没有做ip代理 这里就做简单的降低防止封ip的处理 (亲测爬取的免费代理有些坑，收费的暂时没用到，就没有测试，可以自行测试)
        self.headers = {
            'Host': 'weixin.sogou.com',
            'User-Agent': choice(self.user_agents)
        }


def sgwxCrawl(url, headers):
    res = requests.get(url, headers=headers, timeout=3)
    res.encoding = 'utf-8'  # 注:因为中文会乱码，我们要指定解析网页的编码
    # 用了解析神器 之前一直用 (ps 我是做wbe前端的) 可以自己选择喜欢的解析工具 正则也可以 这些数据并不是层级很深
    result = analysis_url(res.text)
    mongo_base = DataBase()  # 引入mongodb
    mongo_base.add_many(result)


def analysis_url(text):
    html = BeautifulSoup(text, 'lxml').find_all('li')
    data_list = []
    for item in html:
        image = item.find('div', attrs={'class': 'img-box'})  # 这里是找到图片的html元素
        content = item.find('div', attrs={'class': 'txt-box'})  # 这里找到内容的html元素
        # 以下是解析拿需要的数据，就不细说了
        url = image.find('a')['href']
        image_url = 'http:' + image.find('img')['src']
        title = content.find('a').get_text()
        desc = content.find('p').get_text()
        # time 这里是个大坑，元素内容是没有的 有一个s属性的时间戳 转换一下就得到了文章的时间（注意拿到的数据是string 要转int）
        # 具体的自行百度time的用法，我这里也是百度了5分钟
        dateline = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(content.find('span', attrs={'class': 's2'})['t'])))
        data = {
            'url': url,
            'img_url': image_url,
            'title': title,
            'desc': desc,
            'date': dateline
        }
        data_list.append(data)
    return data_list
    # 返回我们整理好的字典数据


def main():
    prepareThings = CeawlInit()
    for link in prepareThings.new_list:
        sgwxCrawl(link, prepareThings.headers)
        print('当前完成列表中第 %s 的爬取' % link)
        time.sleep(1)
    print('完成收工')


if __name__ == '__main__':
    main()
