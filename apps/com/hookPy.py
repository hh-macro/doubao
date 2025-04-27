# -- coding: utf-8 --
# @Author: 胡H
# @File: hook_py.py
# @Created: 2025/4/25 17:43
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: hook

import subprocess
from pathlib import Path

from apps import current_file, logger


def frida_hook(package_name, script_path):
    """
    在 Python 中执行 Frida Hook
    参数:
        package_name: 要 Hook 的安卓应用包名，如 com.aitutor.hippo
        script_path: Frida JS 脚本路径，如 ztool/byteDance.js
    """

    # 构建 Frida 命令
    command = [
        "frida",
        "-U",  # 使用 USB 设备
        "-f", package_name,  # 启动应用程序
        "-l", script_path,  # 加载脚本
        # "--no-pause"  # 自动启动主活动
    ]

    try:
        # 启动 Frida 进程
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # 实时输出处理
        logger.info(f"\n[+] 开始 Hook 应用: {package_name}")
        print("=" * 60)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # 获取退出码
        return_code = process.poll()
        if return_code != 0:
            logger.error(f"\n[!] Frida 进程异常退出，返回码: {return_code}")
            print("错误信息:")
            print(process.stderr.read())

    except FileNotFoundError:
        logger.debug("[!] 未找到 frida 命令，请确保已正确安装 Frida")
        print("安装方法: pip install frida-tools")
    except KeyboardInterrupt:
        logger.success("\n[!] 用户中断操作")
    except Exception as e:
        logger.error(f"[!] 发生未知错误: {str(e)}")


if __name__ == "__main__":
    # 执行 Hook
    frida_hook("com.aitutor.hippo", Path(current_file, "status/byteDance.js"))
