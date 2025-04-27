# -- coding: utf-8 --
# @Author: 胡H
# @File: AdbDevices.py
# @Created: 2025/4/27 9:39
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import subprocess


def adb_devices():
    adbDevices = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                check=True)
    devices = []
    lines = adbDevices.stdout.strip().split('\n')
    for line in lines:
        # 跳过标题行和空行
        if line.strip() and not line.startswith('List of devices'):
            # 通常设备信息的格式是 "设备序列号    设备状态"
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == 'device':
                devices.append(parts[0])

    return devices[0]


if __name__ == '__main__':
    print(adb_devices())
