# -- coding: utf-8 --
# @Author: 胡H
# @File: main_auto.py
# @Created: 2025/1/21 11:08
# @LastModified: 2025/4/25
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import time
from intercept import stop_mitmdump, start_mitmdump
from auto_hold import hold_folder, print_red


def main_auto():
    open("image_cache", "w").close()  # 清空缓存文件
    # 启动子进程
    mitmdump_process = start_mitmdump()  # 启动 mitmdump
    time.sleep(10)
    print("等待 10 秒加载 ......")
    try:
        print("开始运行主程序--\t hold_folder() ")
        print("-" * 60)
        time.sleep(3)
        hold_folder()  # 主进程
    except Exception as e:
        print_red(f"hold_folder() 函数运行时发生异常: {e}")
    finally:
        # 关闭子进程
        time.sleep(15)
        print("-" * 60)
        stop_mitmdump(mitmdump_process)  # 关闭 mitmdump
        print("关闭 mitmdump 子进程\t 主进程结束运行...")


if __name__ == "__main__":
    main_auto()
