from bs4 import BeautifulSoup
import requests
import json
import time
from random import choice
from database_list import DataBase  # 这里是小说分类的db
import pymongo

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
]


def getClassifyData():  # 这个函数主要是爬取网站的排行榜信息 存储到数据库 爬取小说内容就可以从数据库操作，减少不必要的网络请求也为了以后获取小说更新章节更为方便
    url = 'http://www.biquge.com.tw/paihangbang/allvote.html'  # 这里是笔趣阁小说网的阅读排行榜
    headers = {
        'Host': 'www.biquge.com.tw',
        'User-Agent': choice(user_agents)
    }
    res = requests.get(url=url, headers=headers, timeout=10)
    res.encoding = 'gbk'
    data_name = ['fantasy', 'coatard', 'metropolis',
                 'history', 'webgame', 'science', 'terror']  # 这里新建七个分类，去除掉全本小说排行榜
    html = BeautifulSoup(res.text, 'lxml').find_all(
        'div', attrs={'class': 'box'})  # 这里解析出来所有排行榜的html元素集合
    data_list = []  # 七大榜单信息存储的list
    for i in range(0, 7):
        # 新建分类字典元素，区分不同排行榜的不同数据
        data_dict = {'classify': data_name[i], 'list': []}
        for j in html[i].find_all('li'):
            data_dict['list'].append(
                {'url': j.a['href'], 'name': j.a.get_text()})  # 这里是获取各个分类中得小说信息
        data_list.append(data_dict)  # 添加进list里面
    return data_list


def main():
    result = getClassifyData()
    for sub in result:
        client = DataBase(sub['classify'])
        print('%s 分类存储完成' % sub['classify'])
        client.add_many(sub['list'])
    print('存储完成')


if __name__ == '__main__':
    main()
