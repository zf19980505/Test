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
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.util = Data_conversion()
        yeshen = conf.get('DEFAULT', 'air_yeshen')
        if not cli_setup():
            api.auto_setup(__file__, logdir=None, devices=[yeshen])
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        cls.driver = webdriver.Chrome()
        # 万色城二期总部后台
        cls.wsc_admin_url = conf.get('DEFAULT', 'wsc_admin_url')
        # 万色城二期分销后台
        cls.wsc_back_url = conf.get('DEFAULT', 'wsc_back_url')

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Air_Loging = Air_Loging(self.poco, api)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_admin_url + data['el_login_path']
        url2 = self.wsc_back_url + data['el_login_backpath']
        Login.admin, Login.back = self.Login_case.logins(username=data['username'],
                                                         password=data['password'], url=url, url2=url2, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        login2_text = self.Login_case.login2_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问总部首页有误')
        self.assertEqual(first=data['verify'], second=login2_text, msg='访问分销首页有误')

    @file_data('../Data/login.yaml')
    def test_1_xcxlogin(self, **kwargs):
        # 数据处理
        xcx = kwargs['xcx']
        size = self.util.str_lis(xcx['swipe'])
        # 业务
        xcx_login_text = self.Air_Loging.xcx_login(air_el=kwargs['xcx'], air_swipe=size, air_data=xcx['xcx_el_data'])
        # 断言
        self.assertEqual(first=True, second=xcx_login_text, msg='小程序登录失败')

    def test_3_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
