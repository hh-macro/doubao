# -- coding: utf-8 --
# @Author: 胡H
# @File: __init__.py
# @Created: 2025/4/25 14:12
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
from pathlib import Path

import pymongo
import yaml

from apps.com import detection_coord
from apps.protobuf_to import GetByUserInit

# 获取当前文件所在的目录（即 apps 目录）
current_file = Path(__file__).parent  # E:\AAA-project\doubao\apps

with open(Path(current_file, "conf.yaml"), "r", encoding='utf-8') as f:
    CONF = yaml.safe_load(f)

client = pymongo.MongoClient(CONF['mongodb']['url'])

db = client[CONF['mongodb']['db']]
data_list = db[CONF['mongodb']['default']]

data_total = db['data_total']

if __name__ == '__main__':
    print(CONF)
