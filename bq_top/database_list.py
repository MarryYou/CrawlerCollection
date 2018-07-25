import pymongo
# 我用的是mongodb 想用别的这里可以自行选择
# 因为我自己想做几个的爬虫 所以这里就单独定义了一个操作mongo的class
# 主要是因为重复劳动太累了 我懒 不想做。。。
# 没有补充条件查询 时间晚了，以后再改
# 这里是保存各大分类的小说url和小说名字


class DataBase:
    def __init__(self, name):  # 这里先保留 以后再改可配置mongodb 的一些基本信息 现在先写进class 里
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['classify_list']
        self.name = str(name)
        self.collection = self.db[self.name]

    def add_many(self, data):  # 插入多条 传入list
        self.collection.insert_many(data)

    def add_one(self, data):  # 单条插入,传入dict
        self.collection.insert_one(data)

    def get_many(self, info):  # 这里是查询多条,标准格式，自行百度
        doc_list = []
        for item in self.collection.find(info):
            doc_list.append(item)
        return doc_list

    def get_one(self, info):  # 这里是查询单个,标准格式，自行百度
        doc = self.collection.find_one(info)
        return doc
