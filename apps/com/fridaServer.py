# -- coding: utf-8 --
# @Author: 胡H
# @File: fridaServer.py
# @Created: 2025/4/27 9:16
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 启动frida-server服务

import subprocess
import time
from multiprocessing import Process


def frida_server():
    """启动 frida-server"""
    try:
        # 终止已存在的 frida-server
        subprocess.run(
            ["adb", "shell", "su", "-c", "pkill -9 frida-server"],
            check=True,
            timeout=5
        )
    except subprocess.CalledProcessError:
        pass  # 忽略未找到进程的错误

    # 设置权限
    subprocess.run(
        ["adb", "shell", "su", "-c", "chmod 755 /data/local/tmp/frida-server-16.5.9-android-arm64"],
        check=True
    )

    # 启动 frida-server（非阻塞）
    proc = subprocess.Popen(
        ["adb", "shell", "su -c 'cd /data/local/tmp && ./frida-server-16.5.9-android-arm64 &'"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 验证启动状态
    time.sleep(3)
    result = subprocess.run(
        ["adb", "shell", "pgrep -f frida-server"],
        stdout=subprocess.PIPE
    )
    if not result.stdout:
        raise RuntimeError("Frida-server 启动失败")


def run_frida_server():
    """在子进程中运行 frida_server"""
    frida_server()


def start_frida_server():
    """启动 frida_server 子进程并返回进程对象"""
    proc = Process(target=run_frida_server)
    proc.start()
    return proc


def stop_frida_server(proc):
    """终止 frida_server 子进程"""
    proc.terminate()
    proc.join()


if __name__ == "__main__":
    # 启动 frida_server 子进程
    server_proc = start_frida_server()
    print("Frida-server 正在运行...")
    input("按 Enter 键终止服务...")
    # 终止 frida_server 子进程
    stop_frida_server(server_proc)
