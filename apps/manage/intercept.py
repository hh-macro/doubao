import base64
import json
import time
from datetime import datetime
from mitmproxy.tools.main import mitmdump
import subprocess  # 导入 subprocess 模块用于启动和关闭 mitmdump
from mitmproxy import http

# 用于存储所有 base64 编码的字符串
base64_list = []
search_list = []


def image_cache_r():
    # 从缓存文件读取图片名
    with open("image_cache", "r") as cache_file:
        cached_image_name = cache_file.read()
    return cached_image_name


def response(flow: http.HTTPFlow) -> None:
    if (
            "zijieapi.com" in flow.request.url and "https://imapi-oth.zijieapi.com/v1/message/get_by_user" in flow.request.url):
        # print(flow.request.url)
        time.sleep(5)
        flow_res = flow.response.content
        base64_str = base64.b64encode(flow_res).decode('utf-8')
        # print(base64_str)
        key = image_cache_r()
        if key:
            # 创建字典并添加到列表中
            base64_list.append({key: base64_str})
            # print(base64_str)
            save_base64_strings_to_file('base64_strings.json')  # 保存
        else:
            print("截取到包，但程序并未运行---为错误包")

    if (
            "api5-normal-lq.hippoaixue.com" in flow.request.url and "https://api5-normal-lq.hippoaixue.com/hippo/turing/qs/v1/detection/get_or_create" in flow.request.url):
        time.sleep(3)
        try:
            flow_json = flow.response.json()
            search_pieces_list = flow_json['question_search']['search_pieces']
            key = image_cache_r()
            if key:
                for search_pieces in search_pieces_list:
                    search_list.append({
                        'image_name': key,
                        'conversation_id': search_pieces['conversation_id'],
                        'pos': search_pieces['pos']
                    })
                with open('search_message_list.json', 'w') as f:
                    json.dump(search_list, f, indent=4)
                print(f"search_message_list 列表已成功保存......")
            else:
                print("截取到search_message_list 列表, 但程序并未运行---为错误包")
        except Exception as e:
            print(e)
            return


def save_base64_strings_to_file(file_path):
    # 保存 base64_strings 到文件
    with open(file_path, 'w') as file:
        json.dump(base64_list, file, indent=4)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_time}:\t 文件覆盖保存成功！ ------  {file_path}")


# 新增函数：启动 mitmdump
def start_mitmdump():
    # 启动 mitmdump 并加载当前脚本
    mitmdump_cmd = ["mitmdump", "-q", "-s", __file__]
    mitmdump_process = subprocess.Popen(mitmdump_cmd)
    print("mitmdump 已启动\t PID:", mitmdump_process.pid)
    return mitmdump_process


# 新增函数：关闭 mitmdump
def stop_mitmdump(process):
    open("image_cache", "w").close()  # 清空缓存文件
    process.terminate()  # 发送终止信号
    process.wait()  # 等待进程结束
    print("mitmdump 已关闭")


"""
mitmdump -q -s intercept.py  ----启动截包
"""

if __name__ == '__main__':
    open("image_cache", "w").close()  # 清空缓存文件
    mitmdump_process = start_mitmdump()  # 启动 mitmdump

    time.sleep(600)
    stop_mitmdump(mitmdump_process)  # 关闭 mitmdump
