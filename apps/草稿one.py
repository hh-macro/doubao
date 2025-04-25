import os
import json
from datetime import datetime
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("localhost", 27017)
db = client['doubao']
data_list = db['data_list']

def pox_file_structure():
    # 加载 JSON 数据
    with open('search_message_list.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 预处理JSON数据，构建查找字典
    pos_dict = {}
    for item in json_data:
        image_name = item['image_name']
        conversation_id = str(item['conversation_id'])  # 转换为字符串以匹配Mongo中的类型
        key = (image_name, conversation_id)
        pos_dict[key] = item['pos']


    for doc in data_list.find():
        # 提取image_name和conversationId
        image_name = doc['image_name']
        conversation_id = str(doc['conversationId'])  # 确保转换为字符串

        # 查找对应的pos
        key = (image_name, conversation_id)
        pos = pos_dict.get(key)

        if pos:
            # 构建文件路径
            base_path = r'D:/aresult/2025-04-24'
            dir_path = os.path.join(base_path, image_name, conversation_id)
            file_path = os.path.join(dir_path, 'pox.txt')
            with open(file_path, 'w') as f:
                f.write(json.dumps(pos))
        else:
            print(f"没有找到与image_name匹配的pos: {image_name},\t conversationId: {conversation_id}")
pox_file_structure()