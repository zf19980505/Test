class BaserRequest:
    def __init__(self, req_driver):
        self.req_driver = req_driver

    # 定义get请求方法
    def get(self, url, headers=None, params=None):
        return self.req_driver.get(url=url, headers=headers, params=params)

    # 定义post请求
    def post(self, url, headers=None, params=None, data=None):
        return self.req_driver.post(url=url, headers=headers, params=params, data=data)

    # 定义DELETE请求
    def delete(self, url, headers=None, params=None, data=None):
        return self.req_driver.delete(url=url, headers=headers, params=params, data=data)