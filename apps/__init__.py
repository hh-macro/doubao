# -- coding: utf-8 --
# @Author: 胡H
# @File: __init__.py
# @Created: 2025/4/25 14:12
# @LastModified: 2025/4/25
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
from pathlib import Path
import pymongo
import yaml
import socket
from loguru import logger
import sys

from apps.com import detection_coord
from apps.protobuf_to import GetByUserInit

# 获取当前文件所在的目录（即 apps 目录）
current_file = Path(__file__).parent  # E:\AAA-project\doubao\apps
project_rootpath = current_file.parent  # E:\AAA-project\doubao

with open(Path(current_file, "conf.yaml"), "r", encoding='utf-8') as f:
    CONF = yaml.safe_load(f)

client = pymongo.MongoClient(CONF['mongodb']['url'])

db = client[CONF['mongodb']['db']]
data_list = db[CONF['mongodb']['default']]  # 操作集合

data_total = db['data_total']  # 总集合

device_id = socket.gethostname()  # 当前设备ID

# ================================= 日志 =====================================
log_dir = Path(project_rootpath)
log_dir.mkdir(parents=True, exist_ok=True)
# 清除默认配置
logger.remove()

# 控制台输出配置
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 文件输出配置（自动轮转）
logger.add(
    log_dir / "init.log",
    rotation="10 MB",  # 每个日志文件最大10MB
    retention="30 days",  # 保留30天日志
    compression="zip",  # 旧日志压缩为zip
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} - {message}",
    level="DEBUG"
)
"""
DEBUG：详细调试信息
INFO：常规流程记录
SUCCESS：关键成功操作
WARNING：需要注意的情况
ERROR：操作错误
CRITICAL：严重系统错误
"""
# ===========================================================================

if __name__ == '__main__':
    print(CONF)
