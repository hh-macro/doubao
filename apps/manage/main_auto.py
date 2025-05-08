# -- coding: utf-8 --
# @Author: 胡H
# @File: main_auto.py
# @Created: 2025/1/21 11:08
# @LastModified: 2025/4/25
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import time
from pathlib import Path

from apps.manage.intercept import stop_mitmdump, start_mitmdump
from apps.manage.auto_hold import hold_folder

from apps import logger, now_path_current_file
from apps.com import frida_hook, start_frida_server, stop_frida_server


def main_auto():
    if not is_json_empty():
        return

    open(Path(now_path_current_file, "image_cache"), "w").close()  # 清空缓存文件
    open(Path(now_path_current_file, "search_message_list.json"), "w").close()  # 清空缓存文件
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


def is_json_empty():
    """
    bool: 如果 JSON 文件内容大于500000，则进行判断返回 False 还是返回 True。
    """
    file_path = Path(now_path_current_file, "base64_strings.json")
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([], file)  # 初始化为空字典

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if len(str(data)) > 500000:
                logger.debug(f'文件内容较多，请确认是否覆盖')
                whether = input('(n:不执行):')
                if whether == 'n':
                    return False
                else:
                    return True
            else:
                return True

    except json.JSONDecodeError:
        logger.error(f"文件 {file_path} 不是有效的 JSON 格式！")
        return False


if __name__ == "__main__":
    main_auto()
