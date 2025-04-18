# -- coding: utf-8 --
# @Author: 胡H
# @File: delete_devices.py
# @Created: 2025/4/17 11:08
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:  删除手机本地文件

import subprocess


def clear_directory(target_folder):
    """ 删除target_folder路径下的所有内容 """
    command = f"adb shell rm -rf {target_folder}/*"
    subprocess.run(command, shell=True, capture_output=True, text=True)
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
    print("正在删除所有文件...")


if __name__ == '__main__':
    # target_folder = "/sdcard/DCIM/Camera"
    target_folder = "/storage/emulated/0/DCIM"
    clear_directory(target_folder)
