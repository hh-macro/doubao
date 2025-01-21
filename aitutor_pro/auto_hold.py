import time
import subprocess
from pathlib import Path
import uiautomator2 as u2


def clear_directory(target_folder):
    """ 删除target_folder路径下的所有内容 """
    command = f"adb shell rm -rf {target_folder}/*"
    subprocess.run(command, shell=True, capture_output=True, text=True)
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
    print("正在删除所有文件...")


def push_directory(destination_folder_on_pc, target_folder):
    """ 将 destination_folder_on_pc 路径内容传入到手机端 target_folder """
    push_command = ["adb", "push", destination_folder_on_pc, target_folder]
    result_1 = subprocess.run(push_command, capture_output=True, text=True, encoding="utf-8")
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    if result_1.returncode == 0:
        subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
        print("文件推送成功！")
        print(result_1.stdout)



d = u2.connect('4310d42b')
d.implicitly_wait(3)

target_folder = "/sdcard/DCIM/Camera"
directory_file = r"D:/atimu"

path = Path(directory_file)
# 遍历目录及其所有子目录
for item in path.rglob("*"):  # rglob("*") 递归所有
    if item.is_file():  # 只处理文件
        print(f"图片:\t{item} 正在处理...")

        d(text='拍题答疑').click_exists()
        d(text='再拍一页').click_exists(timeout=5)
        push_directory(item, target_folder)  # 传入图片
        time.sleep(2)
        d(resourceId='com.aitutor.hippo:id/mj').click_exists()
        d(resourceId='com.aitutor.hippo:id/1g')[0].click()
        clear_directory(target_folder)  # 清空手机目录
        time.sleep(4)
        con_page = d(text='再拍一页').click_exists(timeout=5)
        if not con_page:
            for i in range(7):
                print(i)
                d(text='重试').click_exists(timeout=3)
                time.sleep(1)
            d(text='再拍一页').click_exists(timeout=5)
