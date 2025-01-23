import base64

import requests


headers = {
    "x-vc-bdturing-sdk-version": "3.6.2.cn",
    "sdk-version": "2",
    "x-tt-token": "000f5d4fe7aabb2cf79d6841974fe5f631032d9aa3a8972534516c22235c8d30aed36ccba6444878b38147ca79431fd7fc96b1590d4c5de59c882d5dca345933369ce4aa7ebd5c9f173ca338ab3406de55c427034ec6d1b0de053e0bd09d92030a0c5-1.0.1",
    "passport-sdk-version": "50554",
    "content-type": "application/x-protobuf",
    "x-ss-stub": "AC60ED7A2C40C15B74807990B8522809",
    "x-tt-trace-id": "00-8c917a0709e7570acde16efa2654ffff-8c917a0709e7570a-01",
    "user-agent": "com.aitutor.hippo/30900 (Linux; U; Android 8.1.0; zh_CN; MI 6X; Build/OPM1.171019.011; Cronet/TTNetVersion:6524e03e 2024-06-17 QuicVersion:8915c07c 2024-04-19)",
    "x-argus": "WHpUt7jYI/C+Vy3y+4EwLOVfNv/WcJD0jydyW3SADarPSJOdrCdDHFIVUkJTLPyOod/gKPsrWBBibZ3xV+nXc01ihfPUUyj4lLxSIJKhd28VhGvAw05jZWfknu58btL90CPFqk2tD4e4JqmcdRWtP6rMMDhQHrzCC5PTb8F8Dh6Yzo8g+ApbQgYjDRYyRqIsfjQ3qcZixIk/VjQ8cLOxBmb/qComnBtO9MK1YtfnMXLZ3oEFYdKOJ0wjayMRLYX/okJxSvWK5gUhn/H3jJJyhZEo",
    "x-gorgon": "8404608504057b2f81b43c98589ff53afa9767203c8eaad97ef7",
    "x-helios": "OqGEKXjuDHxRn0fWIr9MIiYD3iGkU1ehNtfETfIXI2wxWx7O",
    "x-khronos": "1737525131",
    "x-ladon": "NJK7NPE2chudgGnyv61LSeBiDy1N7pkn0ktzOcKJusBTUt1g",
    "x-medusa": "iYeQZ73rBQu+9cr8b1ONAkM/6UEnjapP+aU7iPe3YuTKDWbbkFM2DBd+diecaAz0F1v8eYclb0j2UajQZlg/o57Ns2JV/2UcdvcudZhLzyaGs4C2JHEpCJkI48yYFhs0peZSXRxHmFPi6wtf1z/YDQVizou+nNOf2Fm2CH33O5e1M2wtbrhzdMftn4UngqjacuimHDLevtcJvNSLGyBEsePDu+I9yKalHKg1vIZkP6YWF3Y+mffZMX6WwyHb6e6xecd0MaZJmcJHfGFuUfHumAtyHj4NcJisXXd4hvP0Lt31RvLKi7WlJOfnQfdTp2XPT+aQwEXMQiWPPLziw7ZJ/3BQiUIQmuACNOi+96h+04CZGabXOsjxyY+AsdwwaLrUAbJ7uFlIpugCC/8+PxWTgKnXam8aVw=="
}
url = "https://imapi-oth.zijieapi.com/v1/message/get_by_user"
params = {
    "device_platform": "android",
    "os": "android",
    "ssmix": "a",
    "_rticket": "1737525131369",
    "cdid": "aec0173e-7ef5-454b-8e42-9a5138cb03a1",
    "channel": "xiaomi_520947",
    "aid": "520947",
    "app_name": "c7b60ef373ddc8a69ee518dca396c304a7a19db3",
    "version_code": "30900",
    "version_name": "3.9.0",
    "manifest_version_code": "30900",
    "update_version_code": "3090005",
    "resolution": "1080*2030",
    "dpi": "440",
    "device_type": "MI 6X",
    "device_brand": "xiaomi",
    "language": "zh",
    "os_api": "27",
    "os_version": "8.1.0",
    "ac": "wifi",
    "timezone": "8",
    "region": "CN",
    "iid": "3059289604252652",
    "device_id": "62099860702"
}
data = '\\x08È\\x01\\x10\x8fë/\\x1a\\x105.1.3.15-alpha.8"5q6KYcD5H0fLUtqDO6zFBjV7JxzB8DA5Cyyg4xZhtbvcVu8DCnlPZV(\\x010\\x00:\\x09501031528B\\x0cÂ\\x0c\\x09\\x08ÃàßÁÑ\x88\x8b\\x03J\\x0b62099860702Z\\x07androidb\\x05MI 6Xj\\x058.1.0r\\x010\x90\\x01\\x02\xa0\\x01\\x00'.encode('unicode_escape')
response = requests.post(url, headers=headers, params=params, data=data)

print(response.text)
print(response)
binary_data = response.content
# print(binary_data)
base64_str = base64.b64encode(binary_data).decode('utf-8')

print(base64_str)
