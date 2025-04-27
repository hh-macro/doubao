# -- coding: utf-8 --
# @Author: 胡H
# @File: SSLHook.py
# @Created: 2025/4/27 14:56
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import time

from apps.com import frida_hook, start_frida_server, stop_frida_server

server_proc = start_frida_server()
time.sleep(5)
frida_hook()
time.sleep(5)
input("按 Enter 键停止 Hook...\n")
stop_frida_server(server_proc)
