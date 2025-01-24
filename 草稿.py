def response(flow: http.HTTPFlow) -> None:
    if "zijieapi.com" not in flow.request.url: return
    target_url = "https://imapi-oth.zijieapi.com/v1/message/get_by_user"

    if target_url in flow.request.url:
        # 获取响应内容
        # print(flow.response.text)

        flow_res = flow.response.content

        base64_str = base64.b64encode(flow_res).decode('utf-8')
        # print(base64_str)
        key = image_cache_r()
        if key:
            # 创建字典并添加到列表中
            # base64_list.append({key: base64_str})
            print(base64_str)
            # save_base64_strings_to_file('base64_strings.json')  # 保存
        else:
            print("截取到包，但程序并未运行---为错误包")