import base64
import time
import requests

headers = {
    'User-Agent': 'com.aitutor.hippo/30900 (Linux; U; Android 8.1.0; zh_CN; MI 6X; Build/OPM1.171019.011; Cronet/TTNetVersion:6524e03e 2024-06-17 QuicVersion:8915c07c 2024-04-19)',
    # 'Accept-Encoding': 'gzip, deflate',
    'x-vc-bdturing-sdk-version': '3.6.2.cn',
    'sdk-version': '2',
    'passport-sdk-version': '50554',
    'content-type': 'application/x-protobuf',
    'x-ss-stub': 'C8071679A6155F0493111B6641326F9F',
    'x-tt-trace-id': '00-63ce48c909e7570acdecd71aa64bffff-63ce48c909e7570a-01',
    'x-argus': 'mWMsYZmITbxmxY93pdDdCm44it/c2fRyoPXkho4l+x/uzgPqpO9DLQ5XMQPiUAsYC4eqmwqNCaysbCsigauZJQJSpJKI6EP0eqV0VuyG54euUnHiLzCRB9L2Q0ycVGFejpwxOxO8PIbWa+SCOsMb8fFg0aXlJ5oE644fExeXc9EROiWThhIUpd6IRuaouAJj4+NsMmdPSovihgWI67fDgn26AmzioFsdWyh74X9w4FkYOgG4nDxKCcQzeYN5SzCFzVRG+6Ei/nvVSwD/Jkyo1SG2',
    'x-gorgon': '8404808e0405f6e8a35cab98887a3b4174fc3265634d43db0279',
    'x-helios': '9qqTL2F+x+BePzn6p8CrIUb2uoa0mX/gsodi27zkcM/3nbvL',
    'x-khronos': f'{int(time.time())}',
    'x-ladon': 'BK5PISnoXCSUJbuxS8ArX6DZ03C2dmqWVnB2mSwM8pBleRYW',
    'x-medusa': 'IBiGZxR0EwsXatz8xsybAuqg/0HJUGSd9M9rpCfSQSnFukqgngdROtUroDJvwAQBpqQMwWiRi6LDib3tEe9oLu6OvhrTpo5oIcDAecD9pfZZRem4Lf+H3iatlfDKhqnwlyZug2H6Jg8ZtfTo9Esvet8n3M94BUDe1OARlZDExF58AAX30OdxI/+itauqtF17zE25S20r6P0xQgKzI5rLG8c85Ph45SKPuRFr1VNNOpIxUNalXxi2TmvZAbe2IBsc5+tj/5BSK5+oHf4NAe/WYqowaiVsyawZ8hY86TUT1L2s3dkHKnNoU2qvGLWSAfdwmbvfyR6mTU9hCuPDjbluFq7X7Vf0+GhPdHh2AsQEwZ8HkvJqpcwDBDKRSBN8etulTzJI9aa5hsBtQqTUcxMBEKUXV3W/sA==',
}

with open('C:\\Users\\macroh\\AppData\\Roaming\\Reqable\\tmp\\8ae4ea46-7bc5-42f2-bb3f-40ffed292112', 'rb') as f:
    data = f.read()

# with open(r'E:\AAA-project\muchen_project\豆包爱学\timu\Snipaste_2025-01-13_15-30-46.jpg', 'rb') as f:
#     data = f.read()

response = requests.post(
    f'https://imapi-oth.zijieapi.com/v1/message/get_by_user?device_platform=android&os=android&ssmix=a&_rticket={int(time.time() * 1000)}&cdid=aec0173e-7ef5-454b-8e42-9a5138cb03a1&channel=xiaomi_520947&aid=520947&app_name=c7b60ef373ddc8a69ee518dca396c304a7a19db3&version_code=30900&version_name=3.9.0&manifest_version_code=30900&update_version_code=3090005&resolution=1080*2030&dpi=440&device_type=MI%206X&device_brand=xiaomi&language=zh&os_api=27&os_version=8.1.0&ac=wifi&timezone=8&region=CN&iid=3059289604252652&device_id=62099860702',
    headers=headers,
    data=data,
)

binary_data = response.content
base64_str = base64.b64encode(binary_data).decode('utf-8')

print(base64_str)
