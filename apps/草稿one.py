from pymongo import MongoClient
from datetime import datetime


def copy_collection_with_timestamp(data_total='data_total'):
    """ 源集合data_list复制到新集合并添加时间字段 data_total为目标总集合"""

    current_timestamp = datetime.now()
    # print(current_timestamp)
    # 复制数据并添加时间字段
    documents = data_list.find()
    copied_documents = []
    for doc in documents:
        # 复制文档并添加时间字段
        new_doc = doc.copy()
        new_doc['timestamp'] = current_timestamp
        copied_documents.append(new_doc)

    # 插入到目标集合
    if copied_documents:
        db[data_total].insert_many(copied_documents)
        print(f"已成功将`data_list`复制 {len(copied_documents)} 出总集合中")
    else:
        print("源集合中没有数据。")


# 调用函数
copy_collection_with_timestamp()
