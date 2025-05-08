# -- coding: utf-8 --
# @Author: 胡H
# @File: quality_script.py
# @Created: 2025/5/8 9:57
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 质检脚本

import os
from pathlib import Path


class QualityChecker:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.problem_folders = set()  # 使用集合避免重复
        self.REQUIRED_FILES = {
            'pox_txt': 'pox.txt',  # 精确文件名
            'json_ext': '.json'  # 后缀名
        }

    def check_directory(self):
        """主检查方法"""
        # 遍历一级文件夹
        for l1_folder in self._get_subfolders(self.root_path):
            has_problem = False

            # 遍历二级文件夹
            for l2_folder in self._get_subfolders(l1_folder):
                # 检查图片文件
                if not self._has_image_files(l1_folder):
                    print(f'当前文件夹下找不到图片{l1_folder}')
                    self._add_problem_folder(l1_folder)
                    has_problem = True
                    break  # 跳出二级循环

                # 检查必要文件
                if not self._check_required_files(l2_folder):
                    print(f'当前文件夹下找不到必要文件{l2_folder}')
                    self._add_problem_folder(l1_folder)
                    has_problem = True
                    break  # 跳出二级循环

            if has_problem:
                continue  # 继续下一个一级文件夹

    def _get_subfolders(self, path):
        """获取指定路径下的直接子文件夹"""
        return [entry for entry in path.iterdir() if entry.is_dir()]

    def _has_image_files(self, folder):
        """检查文件夹是否包含图片文件"""
        return any(file.suffix.lower() in {'.jpg', '.jpeg', '.png'}
                   for file in folder.iterdir() if file.is_file())

    def _check_required_files(self, folder):
        has_pox_txt = False
        has_json = False
        for file in folder.iterdir():
            if file.is_file():
                if file.name == self.REQUIRED_FILES['pox_txt']:
                    has_pox_txt = True
                if file.suffix.lower() == self.REQUIRED_FILES['json_ext']:
                    has_json = True
        return has_pox_txt and has_json

    def _add_problem_folder(self, folder):
        """记录问题文件夹"""
        self.problem_folders.add(folder.name)

    def generate_report(self):
        """生成最终报告"""
        print("发现问题文件夹列表: ")
        for idx, name in enumerate(sorted(self.problem_folders), 1):
            print(f"{idx}. {name}")


if __name__ == "__main__":
    # 使用示例
    checker = QualityChecker(r"D:\aresult\2025-05-08")
    checker.check_directory()
    checker.generate_report()
