import base64
import json
from datetime import datetime
from mitmproxy.tools.main import mitmdump

from mitmproxy import http

# 用于存储所有 base64 编码的字符串
base64_strings = []


def response(flow: http.HTTPFlow) -> None:
    target_url = "https://imapi-oth.zijieapi.com/v1/message/get_by_user?device_platform=android&"
    if target_url in flow.request.url:
        # 获取响应内容
        flow_res = flow.response.content

        # 将响应内容编码为 base64 字符串
        base64_str = base64.b64encode(flow_res).decode('utf-8')

        # 将 base64 字符串添加到列表中
        base64_strings.append(base64_str)

        # 打印 base64 字符串
        # print(base64_str)
        save_base64_strings_to_file('base64_strings.json')


# 保存 base64_strings 到文件
def save_base64_strings_to_file(file_path):
    with open(file_path, 'w') as file:
        json.dump(base64_strings, file)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_time}:\t 文件保存成功！ ----  {file_path}")


def mit_main():
    # 启动 mitmdump 并加载当前脚本
    mitmdump(["-q", "-s", __file__])


"""
mitmdump -q -s intercept.py  ----启动截包
"""

if __name__ == '__main__':
    mit_main()
