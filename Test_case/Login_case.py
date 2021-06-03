import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from airtest.core import api
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Page.Login import *
from Util.data_conversion import *
import configparser
from ddt import ddt, file_data


@ddt
class Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.util = Data_conversion()
        if not cli_setup():
            cls.driver = api.auto_setup(__file__, logdir=None, devices=[
                "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
            ])
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        cls.driver = webdriver.Chrome()
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.url = conf.get('DEFAULT', 'url')

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Air_Loging = Air_Loging(self.poco, api)

    @file_data('../Data/login.yaml')
    def test_0_openweb(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.url + data['el_login_path']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/login.yaml')
    def test_1_xcxlogin(self, **kwargs):
        xcx = kwargs['xcx']
        size = self.util.str_lis(xcx['swipe'])
        self.Air_Loging.xcx_login(air_el=kwargs['xcx'], air_swipe=size, air_data=xcx['xcx_el_data'])
        xcx_login_text = self.Air_Loging.xcx_login_text
        self.assertEqual(first='True', second=xcx_login_text, msg='小程序登录失败')


    def test_3_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
