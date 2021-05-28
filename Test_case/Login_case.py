import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from airtest.core.api import *
# from airtest.cli.parser import cli_setup
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Page.Login import *
from ddt import ddt, file_data


@ddt
class Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        # if not cli_setup():
        #     cls.driver = auto_setup(__file__, logdir=True, devices=[
        #         "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
        #     ])
        # cls.test_poco = Airtest_Server(AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False))

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)

    # 传入yaml文件里的数据，通过循环然后把value值转成tuple
    def str_by_tuple(self, data):
        self.lis_key = []
        self.lis_value = []
        for data_key, data_value in dict.items(data):
            self.lis_key.append(data_key)
            str_data = data_value[1: -1]
            str_data_one, str_data_two = str_data.split(',')
            self.tuple_data = (str_data_one, str_data_two)
            self.lis_value.append(self.tuple_data)
        self.zip_obj = zip(self.lis_key, self.lis_value)
        self.dict_data = dict(self.zip_obj)
        return self.dict_data

    @file_data('../Data/login.yaml')
    def test_open(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.str_by_tuple(kwargs['login'])
        self.Login_case.logins(username=data['username'], password=data['password'], url=data['url'], elemter=login_el)
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    def test_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
