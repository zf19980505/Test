from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import unittest
from Page.test import *
import requests
import configparser
import json
from ddt import ddt, file_data


@ddt
class Air_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        #     cls.token = None
        #     conf = configparser.ConfigParser()
        #     conf.read('../Confing/request_confing.ini')
        #     cls.headers = conf.get('DEFAULT', 'headers')
        #     cls.dict_heardes = dict(cls.headers)
        #     print(cls.dict_heardes)
        #     print(type(cls.dict_heardes))
        #     if not cli_setup():
        #         cls.driver = api.auto_setup(__file__, logdir=None, devices=[
        #             "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
        #         ])
        #     cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.url = conf.get('DEFAULT', 'url')
        cls.group_id = None

    def setUp(self):
        self.Req_login = Req_login(requests)

    def str_szie(self, data):
        self.lis_key = []
        self.lis_value = []
        for data_key, data_value in dict.items(data):
            self.lis_key.append(data_key)
            str_data = data_value[1: -1]
            x1, y1, x2, y2 = str_data.split(',')
            size = [x1, y1, x2, y2]
            self.lis_value.append(size)
        self.zip_obj = zip(self.lis_key, self.lis_value)
        self.dict_data = dict(self.zip_obj)
        return self.dict_data

    # @file_data('../Data/login.yaml')
    @file_data('../Data/activity.yaml')
    def test_0_login(self, **kwargs):
        # data = kwargs['data']
        # url = kwargs['url'] + data['req_login_path']
        # self.Req_login.req_login(url=url, data=kwargs['req_login_data'])
        # username = self.Req_login.username
        # self.token = self.Req_login.token
        # self.assertEqual(first=data['username'], second=username, msg='登录成功')
        req_grouop = kwargs['req_grouop']
        path = req_grouop['path']
        data = req_grouop['data']
        data['public_data']['spucode'] = 'SPU2021536910001'
        url = self.url + path['gruop_goods_lis_path']
        # delete_url = self.url + path['delete_group_path']
        self.Req_login.test_group_lis(url=url, params=data['gruop_goods_lis_data'], public_data=data['public_data'])
        Air_test.group_id = self.Req_login.group_id
        self.assertEqual(first='true', second='true', msg='测试')
        # req_grouop['data']['delte_group_data'] = {'id': group_id}
        # self.Req_login.test_dele_group(url=delete_url, params=data['delte_group_data'])
        # delete_text = self.Req_login.delete_text
        # self.assertEqual(first='True', second=delete_text, msg='拼团删除失败，服务器报错')

    @file_data('../Data/activity.yaml')
    def test_1_dele(self, **kwargs):
        req_grouop = kwargs['req_grouop']
        path = req_grouop['path']
        data = req_grouop['data']
        url = self.url + path['delete_group_path']
        req_grouop['data']['delte_group_data'] = {'id': Air_test.group_id}
        self.Req_login.test_dele_group(url=url, params=data['delte_group_data'])
        delete_text = self.Req_login.delete_text
        self.assertEqual(first='True', second=delete_text, msg='拼团删除失败，服务器报错')


if __name__ == '__main__':
    unittest.main()
