# -- coding: utf-8 --
# @Author: 胡H
# @File: algorithm_detection.py
# @Created: 2025/4/21 11:19
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 获取原题坐标

import base64

import requests
import json


def detection_coord(file_name, file_path, timu_file='atimu_all'):
    headers = {
        "accept": "application/json; charset=utf-8",
        "x-vc-bdturing-sdk-version": "3.6.2.cn",
        "sdk-version": "2",
        "x-tt-token": "009017e975fd70f14e049e2efde5b6f02c046166241b75d5caf8c56cc5867360d4de7783c319955c2e7ecd01ec0e65bbc18800f6c3a94b554e2016f33cd8cda09c820998e4a41511dfa7237b972bb8fb6a1fe938a59e0f552dfc0ea02c4ed570d2ded--0a490a20606366dff4a0168479e6d52c8c335500495a9336b9f8df0a03735f0604634f501220db34417cf1448a5129824631d88d347861e0979bbf3cfa7205bdc6e238e1c1b218f6b4d309-3.0.0",
        "passport-sdk-version": "50554",
        "content-type": "application/json; charset=utf-8",
        "x-ss-stub": "CB6E11AEF8A99C6131E138A333634B90",
        "x-ss-dp": "520947",
        "x-tt-trace-id": "00-56590f670dad16005c466999eccaffff-56590f670dad1600-01",
        "user-agent": "com.aitutor.hippo/40500 (Linux; U; Android 11; zh_CN; M2011K2C; Build/RKQ1.200928.002; Cronet/TTNetVersion:5ddc98ee 2025-03-13 QuicVersion:55af8b7a 2024-11-18)",
        "x-argus": "jbCtd3m2htSoNXCA5+q/VOPQXkENkWJdx19vG/riTeXCUwksSojTNIW4FIGcwaT+c2EGaC4oiEYC2ayQKoxUCI5eoqkFOX92aHVs8YPvP1OvNkOYoHqozTAcSht+JO3g/TWm2i6EQ1LcOZhpDFDFRy2t1OCTO5J+xPJgIY5ETHvToIjimq9t64V/Hxos7pSbQI7Eby1ijORJdUFWPcYlAOLrY+f+Brwp1oAfv+8PG/gLgFsfflGnucF5AbAcuK9YUYcZ2tAmbNLymO/X4/7pZI2F",
        "x-gorgon": "8404a094000556f7b0e55f1f3ba837c6592767630f30ba577e02",
        "x-helios": "veqIEEkNr+B+rMU2rFReb67bsZOWKNdt7m1kOL6V4RUvOWQ7",
        "x-khronos": "1745205398",
        "x-ladon": "C35DU5xzfqlekBz7jn0bN9P/Ses8/DmmWrqw+MGrvO4l+KU7",
        "x-medusa": "lLgFaKDUkASjyl/zcmwYDV4AfE7f3CTBd7jcVCKGkVoE2PcIKFy3p0TNmNtN+E/PIZCX2eAtx48joo6PpZhr7C7ISy7vZWBR39Sd/S3Zl/NiMVk1qLRtrn4Cyc0Po9N9En9d+AmJIDT8mDoKG0fhml3h3Be1uEcDG/XwrUNUq4gzaoiulhHWNGeW3JscV4tc6vSHmKsPe74XsaRWZuEA0zW9dkF76UDXeqOtJsnOh8esmpNPl9miC2BAwgPE41Jn/s3LdTIGdEjW/cU1XflG7BCKjRqgx49PFOpmELI1CZ32lLvm2o5qlCakbyrY3HGf/PsZsFpbr7Kf53VxYkixF/aVWUk7eyBmXifCGwZFpMke02mK9YU40uvyWprVBYwdWAztxsdvYoT7+CtsLWcCbg1jDUV7Uw=="
    }
    cookies = {
        "odin_tt": "4a1bb027f001d3cdc3d40a38a4e95bdde77177372187bab25ddbcaa81923b6c2662e5c16b80ca8e00b6a5fa8b3cb1e57c15264fe8b83c8c03178d47b3dafee0d114e3f63f9a97217839bb7dcd2f71734"
    }
    url = "https://api5-normal-lq.hippoaixue.com/hippo/turing/qs/v1/algorithm_detection"
    params = {
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": "1745205398991",
        "cdid": "a2bd9047-895c-4551-b708-1f5c618881f4",
        "channel": "xiaomi_520947",
        "aid": "520947",
        "app_name": "c7b60ef373ddc8a69ee518dca396c304a7a19db3阿",
        "version_code": "40500",
        "version_name": "4.5.0",
        "manifest_version_code": "40500",
        "update_version_code": "4050005",
        "resolution": "1440*3007",
        "dpi": "560",
        "device_type": "M2011K2C",
        "device_brand": "Xiaomi",
        "language": "zh",
        "os_api": "30",
        "os_version": "11",
        "ac": "wifi",
        "timezone": "8",
        "region": "CN",
        "iid": "3044960110933657",
        "device_id": "3044960110929561"
    }

    with open(f'D:/{timu_file}/{file_name}.jpg', "rb") as image_file:
        image_data = image_file.read()

    base64_encoded_data = base64.b64encode(image_data)
    base64_message = base64_encoded_data.decode('utf-8')

    # print(base64_message)

    data = {
        "business_type": 1,
        "detection_type": 2,
        "ImageDatas": [
            {
                "ImageData": base64_message
            }
        ],
        "ProcessTypes": [
            4
        ],
        "ReturnQuestionImages": False,
        "scene_type": 201,
        "TraceId": ""
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    QuestionBoxes = json.loads(response.text)['QuestionBoxes'][0]
    Pos_list = []

    for QuestionBoxe in QuestionBoxes:
        Pos = QuestionBoxe.get('Pos', {})
        Pos_list.append(Pos)

    with open(f'{file_path}/QuestionBoxes.txt', 'w') as f:
        for Pos in Pos_list:
            f.write(f'{Pos}\n')

    if Pos_list:
        print('坐标已成功保存到本地中......')
    return Pos_list


if __name__ == '__main__':
    detection_coord(file_name='file_aliyun@1bba98a2-6239-4be1-8965-b225570423b2-5949', file_path='D:/atimu')
