# -- coding: utf-8 --
# @Author: 胡H
# @File: main_auto.py
# @Created: 2025/1/21 11:08
# @LastModified: 2025/4/25
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import time
from apps.manage.intercept import stop_mitmdump, start_mitmdump
from apps.manage.auto_hold import hold_folder

from apps import logger
from apps.com import frida_hook, start_frida_server, stop_frida_server


def main_auto():
    open("image_cache", "w").close()  # 清空缓存文件
    open("search_message_list.json", "w").close()  # 清空缓存文件
    # 启动子进程
    mitmdump_process = start_mitmdump()  # 启动 mitmdump
    time.sleep(10)
    print("等待 10 秒加载 ......")
    try:
        logger.info("开始运行主程序--\t hold_folder() ")
        print("-" * 60)
        time.sleep(3)
        hold_folder()  # 主进程
        logger.success("程序正常退出")
    except Exception as e:
        logger.critical("程序异常终止", exc_info=True)
        raise
    finally:
        # 关闭子进程
        time.sleep(15)
        print("-" * 60)
        stop_mitmdump(mitmdump_process)  # 关闭 mitmdump

        print("关闭 mitmdump 子进程及 frida 子进程\t 主进程结束运行...")


if __name__ == "__main__":
    main_auto()
