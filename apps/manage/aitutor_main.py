# -- coding: utf-8 --
# @Author: 胡H
# @File: aitutor_main.py
# @Created: 2025/1/21 11:08
# @LastModified: 2025/4/25
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import base64
import json
import os
import re
import shutil
import time
from pathlib import Path
from datetime import datetime
import requests
from bson.json_util import dumps
from bson import json_util
from collections import defaultdict

from apps import CONF, data_list, data_total, db, logger, current_file, now_path_current_file
from apps.com import detection_coord
from apps.protobuf_to import GetByUserInit

aresult = CONF['processor']['result']
source_file_all = CONF['processor']['source_file_all']


# 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址
def re_mango():
    """ 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址 """
    pattern1 = re.compile(r'https:(.*?).png', re.IGNORECASE)
    pattern2 = re.compile(r'!\[img\]\(https:(.*?)\)', re.IGNORECASE)

    datee_name = datetime.now().strftime("%Y-%m-%d")  # 当前时间

    # 定义替换逻辑
    def dynamic_replacement(match, pattern_type, conversationId, image_name):
        if pattern_type == 1:  # 第一种格式
            rout_img = 'https:' + match.group(1) + '.png'
        else:  # 第二种格式
            rout_img = 'https:' + match.group(1)
        try:
            # print('rout_img:\t', rout_img)
            image_content = requests.get(rout_img).content
            png_name = int(time.time() * 1000000)
            path_pg = os.path.join(aresult, datee_name, image_name, conversationId, f"{png_name}.png")
            with open(path_pg, 'wb') as f:
                f.write(image_content)
            # print(f'{rout_img} ----保存成功')

            if pattern_type == 2:
                return f"<img src='/{path_pg}' />"
            return f"/{path_pg}"
        except Exception as e:
            logger.error(f"{e}-----------------图片下载发送异常--返回原值")

    print('开始匹配图片地址......')
    # 遍历集合中的文档
    for document in data_list.find():
        try:
            # rich_text = document['qa_biz_params']['qa_item_result']  # 确保提取字段内容
            rich_text = document.get('stem')  # 确保提取字段内容
            answer_text = document.get('answer')  # 确保提取answer字段内容
            analysis_text = document.get('analysis')  # 确保提取analysis字段内容
            conversationId = document.get('conversationId')  # 确保提取conversationId字段内容
            image_name = document.get('image_name')  # 确保提取analysis字段内容
            # print('rich_text:\t', rich_text)

            # 初始化原始字符串和替换后的变量
            rich_text_str = json.dumps(rich_text, ensure_ascii=False) if rich_text is not None else None
            answer_text_str = json.dumps(answer_text, ensure_ascii=False) if answer_text is not None else None
            analysis_text_str = json.dumps(analysis_text, ensure_ascii=False) if analysis_text is not None else None

            new_text = rich_text_str
            new_answer = answer_text_str
            new_analysis = analysis_text_str
            # 处理analysis字段
            if analysis_text is not None:
                if pattern2.search(analysis_text_str):
                    print("-匹配到第二种格式的 URL (analysis)，进行替换")
                    new_analysis = pattern2.sub(lambda m: dynamic_replacement(m, 2, conversationId, image_name),
                                                analysis_text_str)
                elif pattern1.search(analysis_text_str):
                    print("-匹配到第一种格式的 URL (analysis)，进行替换")
                    new_analysis = pattern1.sub(lambda m: dynamic_replacement(m, 1, conversationId, image_name),
                                                analysis_text_str)
                # else:
                #     print("-未匹配到任何 URL (analysis)，跳过替换")
            # print(new_analysis)
            # 处理answer字段
            if answer_text is not None:
                if pattern2.search(answer_text_str):
                    print("-匹配到第二种格式的 URL (answer)，进行替换")
                    new_answer = pattern2.sub(lambda m: dynamic_replacement(m, 2, conversationId, image_name),
                                              answer_text_str)
                elif pattern1.search(answer_text_str):
                    print("-匹配到第一种格式的 URL (answer)，进行替换")
                    new_answer = pattern1.sub(lambda m: dynamic_replacement(m, 1, conversationId, image_name),
                                              answer_text_str)
                # else:
                #     print("-未匹配到任何 URL (answer)，跳过替换")

            # 处理stem字段
            if rich_text is not None:
                if pattern2.search(rich_text_str):
                    print("-匹配到第二种格式的 URL (stem)，进行替换")
                    new_text = pattern2.sub(lambda m: dynamic_replacement(m, 2, conversationId, image_name),
                                            rich_text_str)
                elif pattern1.search(rich_text_str):
                    print("-匹配到第一种格式的 URL (stem)，进行替换")
                    new_text = pattern1.sub(lambda m: dynamic_replacement(m, 1, conversationId, image_name),
                                            rich_text_str)
                # else:
                #     print("-未匹配到任何 URL (stem)，跳过替换")

            # 更新MongoDB文档
            update_data = {}
            if rich_text is not None and new_text != rich_text_str:
                update_data['stem'] = json.loads(new_text)
            if answer_text is not None and new_answer != answer_text_str:
                update_data['answer'] = json.loads(new_answer)
            if analysis_text is not None and new_analysis != analysis_text_str:
                update_data['analysis'] = json.loads(new_analysis)

            if update_data:
                data_list.update_one(
                    {"_id": document["_id"]},
                    {"$set": update_data}
                )
                print(f"文档已更新：{update_data.keys()}")
                # print("-" * 40)
            # else:
            #     print("文档未更改")

        except Exception as e:
            logger.error(f"处理文档时发生异常: {e}")
            continue

        # print("原文本:")
        # print(rich_text_str)
        # print("替换后的文本:")
        # print(new_text)

        # 将替换后的内容保存回 MongoDB
        try:
            if new_text != rich_text_str:
                updated_rich_text = json.loads(new_text)
                data_list.update_one(
                    {"_id": document["_id"]},
                    {"$set": {
                        "stem": updated_rich_text
                    }}
                )
                print("文档对图片地址(stem)----已更新")
            if new_answer != answer_text_str:
                updated_answer_text = json.loads(new_answer)
                data_list.update_one(
                    {"_id": document["_id"]},
                    {"$set": {
                        "answer": updated_answer_text
                    }}
                )
                print("文档对图片地址 (answer)----已更新")
            if new_analysis != analysis_text_str:
                updated_analysis_text = json.loads(new_analysis)
                data_list.update_one(
                    {"_id": document["_id"]},
                    {"$set": {
                        "analysis": updated_analysis_text
                    }}
                )
                print("文档对图片地址 (analysis)----已更新")
            # else:
            #     print("文档未更改")

            # print("-" * 40)
        except Exception as e:
            logger.error(f"更新 MongoDB 文档时发生异常：{e}")


def empty_mongo(bank):
    # 清空指定集合中的所有文档
    bank.delete_many({})


# 文本前面加上红色前缀
def print_red(text):
    """ 文本前面加上红色前缀"""
    RED = "\033[31m"  # 红色
    RESET = "\033[0m"  # 重置颜色
    print(f"{RED}{text}{RESET}")


# 获取当前 年-月-日
def time_date():
    """ 获取当前 年-月-日"""
    current_datetime = datetime.now()
    return f"{current_datetime.year}-{current_datetime.month}-{current_datetime.day}"


# 检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。
def create_parent_and_children():
    """  检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。"""
    datee_name = time_date()
    parent_folder = rf"{aresult}/{datee_name}"
    parent_path = Path(parent_folder)

    # 检查父文件夹是否存在，如果不存在则创建
    if not parent_path.exists():
        print(f"父文件夹 {parent_folder} 不存在，正在创建父文件夹及其子文件夹...")
        parent_path.mkdir(parents=True, exist_ok=True)  # 创建父文件夹
        # 创建所有子文件夹
        # for child in child_folders:
        #     (parent_path / child).mkdir(exist_ok=True)
        #     print(f"已创建子文件夹：{parent_folder}/{child}")


# 对base64_strings.json 文件里面的base64编码进行去重操作
def the_frist():
    """ 对 base64_strings.json 文件里面的 base64 编码进行去重操作，同时保留原始的键 """
    file_path = Path(now_path_current_file, 'base64_strings.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表（列表中套字典）

        # 提取所有键值对
        key_value_pairs = [(list(item.keys())[0], list(item.values())[0]) for item in base64_list]

        # 去重操作：根据值（value）去重，但保留第一个出现的键（key）
        unique_values = set()
        unique_key_value_pairs = []
        for key, value in key_value_pairs:
            if value not in unique_values:
                unique_values.add(value)
                unique_key_value_pairs.append((key, value))

        # 将去重后的键值对重新包装为列表中套字典的形式
        unique_base64_list = [{key: value} for key, value in unique_key_value_pairs]

        # 保存去重后的数据到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(unique_base64_list, file, ensure_ascii=False, indent=4)

        print(f"对 {file_path} 去重结果已经重新覆盖保存")
        print('-' * 51)
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在！")
    except json.JSONDecodeError:
        logger.error(f"文件 {file_path} 内容为空或格式错误！")


# 读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法
def circulate():
    """ 读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法 """
    file_path = Path(now_path_current_file, "base64_strings.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表（列表中套字典）
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在/位置错误！")
        base64_list = []
    except json.JSONDecodeError:
        logger.error(f"JSON 解析错误: 大概率是 {file_path} 内容为空")
        base64_list = []

    # 遍历列表中的每个字典
    for i, item in enumerate(base64_list, start=1):
        for key_cache, base64_str in item.items():  # 提取字典中的键和值
            if len(base64_str) > 3000:
                print(f"第 {i} 个条目(键: {key_cache})的 base64 字符串长度超过 3000，正在处理...")
                unpack(base64_str, key_cache)  # 调用 unpack 方法处理
                print("---------------------------------------------------")


# # 打开文件并清空内容
def clear_json_file(file_path):
    # 打开文件并清空内容
    with open(file_path, "w", encoding="utf-8") as file:
        file.truncate()  # 清空文件内容
    print(f"文件 {file_path} 的内容已被完全清空。")


# 对data_list'表中的内容进行去重操作
def de_weigh_json():
    pipeline = [
        {
            "$project": {
                # 定义分组键：优先按 stem 内容分组，次之按 analysis，最后按 answer
                "group_key": {
                    "$cond": [
                        # 第一层条件：stem 存在且内容非空
                        {"$and": [
                            {"$ne": ["$stem", None]},
                            {"$ne": ["$stem", ""]},
                            {"$ifNull": ["$stem", False]}  # 确保字段存在
                        ]},
                        {"type": "stem", "value": "$stem"},  # 标记为 stem 类型

                        # 第二层条件（嵌套）：analysis 存在且内容非空（且 stem 不存在）
                        {"$cond": [
                            {"$and": [
                                {"$ne": ["$analysis", None]},
                                {"$ne": ["$analysis", ""]},
                                {"$ifNull": ["$analysis", False]}
                            ]},
                            {"type": "analysis", "value": "$analysis"},  # 标记为 analysis 类型

                            # 默认分支：使用 answer（且前两者都不存在）
                            {"type": "answer", "value": "$answer"}
                        ]}
                    ]
                },
                # 保留所有必要字段
                "stem": 1,
                "answer": 1,
                "analysis": 1,
                "stem_title": 1,
                "answer_title": 1,
                "analysis_title": 1,
                "conversationId": 1,
                "image_name": 1
            }
        },
        {
            "$group": {
                "_id": "$group_key",  # 按复合键分组（类型+值）
                "documents": {"$push": "$$ROOT"}
            }
        },
        {
            "$addFields": {
                "documents": {
                    "$map": {
                        "input": "$documents",
                        "as": "doc",
                        "in": {
                            "doc": "$$doc",
                            # 计算字段完整性得分（包含标题字段）
                            "field_score": {
                                "$add": [
                                    {"$cond": [{"$and": [{"$ne": ["$$doc.stem", None]}, {"$ne": ["$$doc.stem", ""]}]},
                                               2, 0]},  # stem 权重更高
                                    {"$cond": [
                                        {"$and": [{"$ne": ["$$doc.analysis", None]}, {"$ne": ["$$doc.analysis", ""]}]},
                                        1, 0]},
                                    {"$cond": [
                                        {"$and": [{"$ne": ["$$doc.answer", None]}, {"$ne": ["$$doc.answer", ""]}]}, 1,
                                        0]},
                                    {"$cond": [{"$ne": ["$$doc.stem_title", None]}, 1, 0]},  # 标题字段加分
                                    {"$cond": [{"$ne": ["$$doc.answer_title", None]}, 1, 0]},
                                    {"$cond": [{"$ne": ["$$doc.analysis_title", None]}, 1, 0]}
                                ]
                            }
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "documents": {
                    "$sortArray": {
                        "input": "$documents",
                        "sortBy": {"field_score": -1}  # 按得分降序排序
                    }
                }
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {"$arrayElemAt": ["$documents.doc", 0]}  # 保留得分最高的文档
            }
        }
    ]
    unique_documents = list(data_list.aggregate(pipeline))

    # 提取唯一文档的 _id 列表
    unique_ids = [doc["_id"] for doc in unique_documents]

    # 删除集合中不在唯一列表中的文档
    original_count = data_list.count_documents({})
    result = data_list.delete_many({"_id": {"$nin": unique_ids}})
    deduplicated_count = data_list.count_documents({})

    # 打印去重结果
    print(f"原始集合文档数量: {original_count}")
    print(f"删除的重复文档数量: {result.deleted_count}")
    print(f"去重后集合文档数量: {deduplicated_count}")
    print("-" * 51)


# 检查字符串是否包含中文字符
def contains_chinese(s):
    """检查字符串是否包含中文字符"""
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 将 unpack() 方法筛选成功的list追加存入 data_list.json 文件中"
def json_save_base64(filtered_list, key_cache):
    """ 将 unpack() 方法筛选成功的list存入 data_list表中"""
    jso1_list = [saw2 for saw2 in filtered_list]
    # print('jso1_list\t', len(jso1_list), jso1_list)
    # 向每个字典中添加一个新的键值对
    for item in jso1_list:
        item["image_name"] = key_cache

    try:
        result_dict = data_list.insert_many(jso1_list)
    except TypeError as e:
        print_red(jso1_list)
        logger.error(f"数据转换或插入 MongoDB 表时发生了 Type Error: {e}")
        return
    print(f"已成功向 data_list 表中插入 {len(result_dict.inserted_ids)} 条数据。")


# 将mango表中数据转json
def mango_json():
    # 将mango表中数据转json
    documents = list(data_list.find({}))
    datee_name = time_date()  # 当前时间
    try:
        # 将文档导出为 JSON 文件
        with open(f"{aresult}/{datee_name}/data_list.json", "w", encoding="utf-8") as outfile:
            outfile.write(dumps(documents, ensure_ascii=False))
        print("data_list.json导出成功")
    except Exception as e:
        logger.error(f"数据转换或导出 JSON 表时发生了 Exception: {e}")


# 核心方法unpack() 对读取的 base64码  进行转换识别操作，再通过层层筛选，得到所需josn结果
def unpack(base64_str, key_cache):
    """ 核心方法 对读取的 base64码  进行转换识别操作，再通过层层筛选，得到所需josn结果 """
    dict_result = GetByUserInit().parse(base64.b64decode(base64_str)).to_json(indent=2)
    # print(dict_result)
    filtered_messages = []  # 存放 dict_result 包含中文的字段 ----> 此内容存放 未合并 未转换 的原始数据
    json_data = json.loads(dict_result)

    for inner_message in json_data.get("innerList", []):
        nested = inner_message.get("nested", {})
        deep_nested = nested.get("deepNested", [])
        for dn_message in deep_nested:
            card_stem = dn_message.get("cardStem", "")
            prompt_content = dn_message.get("promptContent", [])

            # 过滤 promptContent 中包含中文字符的 conText
            filtered_prompt_content = [
                item for item in prompt_content
                if contains_chinese(item.get("conText", ""))
            ]

            # 如果 cardStem 或 filtered_prompt_content 中包含中文字符 则保留该deepNestedMessage
            if contains_chinese(card_stem) or filtered_prompt_content:
                # 更新 dn_message 中的 promptContent 为过滤后的结果
                dn_message["promptContent"] = filtered_prompt_content
                filtered_messages.append(dn_message)

    print('unpack() 第一次处理后数量:', len(filtered_messages), end=" |\t")  # 此内容为未合并为转换的原始数据
    # print(filtered_messages)  # 调试时启用 | 打印信息列表

    # 创建包含 conversationId 和 cardStem 的字典列表
    conversation_card_list = []
    for message in filtered_messages:
        card_stem = message.get('cardStem')
        conversation_id = message.get('conversationId')
        if card_stem and conversation_id:
            conversation_card_list.append({
                'conversationId': conversation_id,
                'cardStem': card_stem
            })

    # 未筛选的值，将cardStem的的字典格式化，然后将同级的conversationId插入将cardStem的的字典格式化中并返回新列表
    processed_data = []
    for conversation_card in conversation_card_list:  # 遍历合并后的 conversation_card_list
        conversationIdTe = conversation_card['conversationId']
        cardStemTe = conversation_card['cardStem']
        cardStemTe_json = json.loads(cardStemTe)
        cardStemTe_json['conversationId'] = conversationIdTe  # 将conversationId插入cardStem
        processed_data.append(cardStemTe_json)  # 追加入新列表

    # print(len(processed_data), end=" ")
    # print(processed_data)
    # con_texts = [item["cardStem"] for item in processed_data if "cardStem" in item]
    # print(con_texts)
    filtered_data = []
    for iteam in processed_data:
        try:
            # 解析 JSON 字符串
            # parsed_item = json.loads(iteam)
            content = iteam.get("content", "")

            # 统计中文字符数量
            chinese_count = len(re.findall(r'[\u4e00-\u9fff]', content))

            # 如果中文字符数量小于 5，则保留
            if chinese_count > 5:
                filtered_data.append(iteam)
        except json.JSONDecodeError as e:
            logger.error(f"解析 JSON 时发生错误: {e}")

    print('unpack() 第二次处理后数量', len(filtered_data), end=" |\t")
    # print(filtered_data)  # 调试时启用 | 打印信息列表

    filtered_list = []
    for index, ie1 in enumerate(filtered_data):
        try:
            # 解析 JSON 字符串
            content_ie1 = ie1.get("content", "")
            content_dict = json.loads(content_ie1)
            # 检查 avatar_text 是否为 "有问题？向豆包提问"
            if ie1['card_type'] == 20:
                continue  # 跳过该条目  20 --> 有问题？向豆包提问

            # 检查 avatar_text 是否为 "有问题？向豆包提问"(双重判断)
            if "avatar_text" in content_ie1:
                if content_dict.get("avatar_text") == "有问题？向豆包提问":
                    continue  # 跳过该条目

            # 如果不满足条件，则保留该条目
            # 将conversationId合并到 content 中并将合并后的content插入新列表中
            conversationIdTr = ie1['conversationId']
            content_dict['conversationId'] = conversationIdTr
            filtered_list.append(content_dict)

        except json.JSONDecodeError as e:
            logger.error(f"解析 JSON 时发生错误: {e}")

    print('unpack() 第三次处理后数量', len(filtered_list), end="\n")
    # print(filtered_list)  # 调试时启用 | 打印信息列表

    json_save_base64(filtered_list, key_cache)  # 存入 data_list 表中


def deduplicate_mongo_data():
    """只移除无用字段"""

    pipeline = [
        # 移除无用字段
        {"$project": {
            "answer_title": 0,
            "stem_title": 0,
            "analysis_title": 0,
            "analysis_loading": 0,
            "retry_attr": 0,
            "allow_edit_stem": 0,
            "CanReasoning": 0,
            "think": 0
        }}
    ]

    # 执行聚合
    updated_data = list(data_list.aggregate(pipeline))

    # 清空原集合并插入更新后的数据
    data_list.delete_many({})
    if updated_data:
        data_list.insert_many(updated_data)
    # print(f"字段清理完成，共保留 {len(updated_data)} 条记录")


def copy_collection_with_timestamp():
    """ 原集合data_list复制到新集合并添加时间字段 data_total为目标总集合"""

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
    try:
        if copied_documents:

            db['data_total'].insert_many(copied_documents)
            print(f"已成功将`data_list`复制 {len(copied_documents)}个数据进入 总集合中")
            print('-' * 40)
        else:
            print_red("源集合中没有数据。")
    except Exception as e:
        logger.error(f"批量写入时发生错误(大概率为值已存在):\t{e}")


def load_search_data():
    """ 读取search_message_list.json并构建映射关系"""
    image_conv_map = defaultdict(set)
    with open(Path(now_path_current_file, 'search_message_list.json'), 'r', encoding='utf-8') as f:
        search_list = json.load(f)
    for item in search_list:
        image_name = item['image_name']
        conv_id = str(item['conversation_id'])  # 转换为字符串类型
        image_conv_map[image_name].add(conv_id)
    return image_conv_map


def clean_mongo_data(image_conv_map):
    """  根据创建好的映射关系image_conv_map 来清理 mango不符合条件的数据"""
    for image_name, allowed_ids in image_conv_map.items():
        # 构造查询条件：匹配当前image_name且conversationId不在允许的列表中的文档
        query = {
            'image_name': image_name,
            'conversationId': {'$nin': list(allowed_ids)}
        }
        result = data_list.delete_many(query)
        print(f"Image: {image_name} - 已删除 {result.deleted_count} 个无效文档")
    print('-' * 51)


class MongoDocProcessor:
    """ 将指定mongo库 保存到本地, 并按指定格式存放"""

    def __init__(self, base_output_dir=aresult):
        self.base_output_dir = base_output_dir

    def copy_image(self, source_path, destination_path):
        # 将一张图片从一个文件夹复制到另一个文件夹
        try:
            shutil.copy2(source_path, destination_path)
        except Exception as e:
            logger.error(f'在文件夹中找不到该需要复制的图片文件 {e}')

    def _read_search_file(self):
        # 加载 JSON 数据
        with open(Path(now_path_current_file, 'search_message_list.json'), 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data

    def _parse_timestamp(self):
        """生成当天日期 ---> 2025-04-18 """
        return datetime.now().strftime("%Y-%m-%d")

    def _get_output_paths(self, doc):
        """生成目标路径"""
        dt = self._parse_timestamp()

        base_dir = os.path.join(self.base_output_dir, dt)
        # target_dir = os.path.join(base_dir, doc["image_name"])
        oid = str(doc['conversationId'])
        # print(oid)
        target_dir = os.path.join(base_dir, doc["image_name"], oid)

        filename = f"{oid}.json"

        return target_dir, filename, oid

    def coordinate(self):
        """ 发起请求, 保存总坐标 | 将题目图片 保存对应题目文件夹中"""
        image_cursor = data_list.find({"image_name": {"$exists": True}}, {"image_name": 1, "_id": 0})
        unique_image_names = set()
        # 遍历查询结果并添加到集合中
        for doc in image_cursor:
            image_name = doc.get("image_name")
            unique_image_names.add(image_name)
        unique_image_names = list(unique_image_names)  # 转换为列表

        for unique_image_name in unique_image_names:
            base_dir = os.path.join(self.base_output_dir, self._parse_timestamp())

            target_dir_new = os.path.join(base_dir, unique_image_name)

            file_name_base = os.path.basename(target_dir_new)
            file_path_dir = os.path.dirname(target_dir_new)
            print('-' * 40)
            try:
                print('总坐标功能仅供开发测试...正式环境不启用')
                # detection_coord(file_name_base, target_dir_new)  # 发起请求, 保存总坐标 注：只开发环境使用
            except Exception as e:
                logger.error(f'请求发送失败 ---->   {e}')
            destination_folder = rf"{source_file_all}\{file_name_base}.jpg"
            source_image = rf'{aresult}\{self._parse_timestamp()}\{file_name_base}\{file_name_base}.jpg'
            print(destination_folder)
            print(source_image)
            self.copy_image(destination_folder, source_image)

    def pox_file_structure(self):
        """  保存坐标到本地"""
        # 预处理JSON数据，构建查找字典
        pos_dict = {}
        for item in self._read_search_file():
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
                base_path = rf'{aresult}/{self._parse_timestamp()}'
                dir_path = os.path.join(base_path, image_name, conversation_id)
                file_path = os.path.join(dir_path, 'pox.txt')
                with open(file_path, 'w') as f:
                    f.write(json.dumps(pos))
            else:
                print_red(f"没有找到与image_name匹配的pos: {image_name},\t conversationId: {conversation_id}")

    def screen_local_file(self):
        """  构建数据结构并清理文件夹 | 去除不在坐标请求对应中的子题目 """
        raw_data = self._read_search_file()

        # 构建目标数据结构
        image_mapping = {}
        for item in raw_data:
            img_name = item.get("image_name")
            conv_id = str(item.get("conversation_id"))  # 统一转为字符串

            if not img_name or not conv_id:
                continue
            if img_name not in image_mapping:
                image_mapping[img_name] = []
            image_mapping[img_name].append(conv_id)

        # print(image_mapping)  # {'': [], '': [],...}
        dt = self._parse_timestamp()
        base_path = rf"{aresult}\{dt}"
        for img_name, valid_ids in image_mapping.items():
            target_dir = os.path.join(base_path, img_name)

            if not os.path.exists(target_dir):  # 跳过不存在的目录
                logger.debug(f"⚠️ 目录不存在: {target_dir}")
                continue
            # 遍历子文件夹
            for folder in os.listdir(target_dir):
                folder_path = os.path.join(target_dir, folder)

                if not os.path.isdir(folder_path):
                    continue  # 跳过文件
                # 删除不在白名单的文件夹
                if folder not in valid_ids:
                    try:
                        shutil.rmtree(folder_path)
                    except Exception as e:
                        logger.error(f"❌ 删除失败:{folder_path} ({str(e)})")
        logger.info('已成功将本地数据结果筛选完毕')

    def process_documents(self, data_list):
        """处理文档主方法"""
        cursor = data_list.find({})  # 查找并将data_list库内容转换为JSON格式
        documents = json_util.loads(json_util.dumps(cursor))
        try:
            for doc in documents:
                target_dir, filename, oid = self._get_output_paths(doc)
                os.makedirs(target_dir, exist_ok=True)

                # print('target_dir:\t', target_dir)
                # D:\aresult\2025-04-21\file_aliyun@1bbce84d-77f0-47b4-a551-8b37a3180751-569\file_aliyun@1bbce84d-77f0-47b4-a551-8b37a3180751-569

                file_path = os.path.join(target_dir, filename)

                with open(file_path, 'w', encoding='utf-8') as f:
                    json_str = json_util.dumps(doc, ensure_ascii=False, indent=2)
                    f.write(json_str)
                # print(f'文档 {oid}\t已成功保存到本地\t{file_path}')
                # logger.error(f"处理文档 {doc.get('_id', '')} 失败: {str(e)}")
        except Exception as e:
            logger.error(f"处理文档 {documents} 失败:\t {str(e)}")
        print(f'data_list 库中所有内容已成功转化到本地 json')

        self.coordinate()
        self.pox_file_structure()
        self.screen_local_file()


def aitutorMain():
    # unpack(base64_str)  # 单个测试 | 弃用

    # create_parent_and_children()  # 检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。 | 弃用
    logger.info("aitutor 程序启动")

    the_frist()  # 对base64_strings.json 文件里面的base64编码进行去重操作

    circulate()  # man

    clean_mongo_data(load_search_data())  # 根据的映射关系来清理 mango 不符合条件的数据

    de_weigh_json()  # 对 data_list 表中的内容进行去重操作

    deduplicate_mongo_data()  # 去掉无用字段

    copy_collection_with_timestamp()  # 原集合data_list复制到新集合并添加时间字段 data_total为目标总集合

    processor = MongoDocProcessor()
    processor.process_documents(data_list)  # 将指定mongo库 保存到本地, 并按指定格式存放 | 保存每个题目的对应坐标  |将题目图片 保存对应题目文件夹中|  清洗不在坐标中的题目  |

    re_mango()  # 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址

    # mango_json()  # mango表转json | 弃用

    empty_mongo(bank=data_list)  # 清空指定集合中的所有文档

    # clear_json_file(file_path="base64_strings.json")  # 删除并重新创建 base64_strings.json

    logger.success("所有数据已全部处理完成")


if __name__ == '__main__':
    aitutorMain()
"""
第二代版本:在筛选的时候，将cardStem保留，去掉下级conText中的内容
        与第一版区别: 题目内容较为清晰, 且题目与AI解答所有页面全在一起

"""
