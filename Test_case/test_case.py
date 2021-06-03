from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import unittest
from Page.test import *
import requests
import configparser
from ddt import ddt, file_data


@ddt
class Air_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not cli_setup():
            cls.driver = api.auto_setup(__file__, logdir=None, devices=[
                "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
            ])
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # conf = configparser.ConfigParser()
        # conf.read('../Confing/request_confing.ini')
        # cls.url = conf.get('DEFAULT', 'url')
        # cls.group_id = None

    def setUp(self):
        self.Airtest_Server = Airtest_Server(self.poco, api)

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

    @file_data('../Data/xcx_group.yaml')
    def test_0(self, **kwargs):
        size = self.str_szie(kwargs['swipe'])
        xcx_el_data = kwargs['xcx_el_data']
        self.Airtest_Server.test_wx(air_el=kwargs['weixin'], air_swipe=size, air_data=xcx_el_data)
        # 断言校验
        xcx_group_text = self.Airtest_Server.xcx_group_text
        self.assertEqual(first='True', second=xcx_group_text, msg='该商品不是拼团商品')

    @file_data('../Data/xcx_group.yaml')
    def test_1(self, **kwargs):
        xcx_el_data = kwargs['xcx_el_data']
        self.Airtest_Server.test_airpay(air_data=xcx_el_data)


if __name__ == '__main__':
    unittest.main()
