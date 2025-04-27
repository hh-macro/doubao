# -- coding: utf-8 --
# @Author: 胡H
# @File: fridaServer.py
# @Created: 2025/4/27 9:16
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 启动frida-server服务
import subprocess


def frida_server():
    # 进入 adb shell 环境
    adb_shell_process = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

    # 在 adb shell 中执行 su 命令获取超级用户权限
    adb_shell_process.stdin.write(b'su\n')
    adb_shell_process.stdin.flush()

    # 切换到目标目录
    adb_shell_process.stdin.write(b'cd /data/local/tmp\n')
    adb_shell_process.stdin.flush()

    # 列出当前目录下的文件和目录
    adb_shell_process.stdin.write(b'ls\n')
    adb_shell_process.stdin.flush()

    # 执行 frida-server
    adb_shell_process.stdin.write(b'./frida-server-16.5.9-android-arm64')
    adb_shell_process.stdin.flush()

    # 读取输出并打印，可以根据需要处理输出
    while True:
        output = adb_shell_process.stdout.readline()
        if output == b'' and adb_shell_process.poll() is not None:
            break
        if output:
            print(output.decode().strip())

    # 等待进程结束
    adb_shell_process.wait()


if __name__ == "__main__":
    frida_server()
