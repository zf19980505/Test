# import requests
import json
import re


class BaserRequest:
    def __init__(self, req_driver):
        self.req_driver = req_driver

    # 定义get请求方法
    def get(self, url, headers=None, params=None):
        return self.req_driver.get(url=url, headers=headers, params=params)

    # 定义post请求
    def post(self, url, headers=None, params=None, data=None):
        if data is not None:
            data = self.json_dumps(data)
        return self.req_driver.post(url=url, headers=headers, params=params, data=data)

    # 请求参数转换为json格式
    def json_dumps(self, params):
        return json.dumps(params)

    # 请求json参数转换为文本格式
    def json_loads(self, params):
        return json.loads(params)







