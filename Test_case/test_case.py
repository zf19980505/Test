from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
import unittest
from Page.test import *
from Page.Login import *
from Page.Coupons import *
from selenium.webdriver.common.keys import Keys
import requests
import configparser
from ddt import ddt, file_data
from Util.data_conversion import *
import datetime


@ddt
class Air_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.util = Data_conversion()
        cls.driver = webdriver.Chrome()
        # if not cli_setup():
        #     cls.driver = api.auto_setup(__file__, logdir=None, devices=[
        #         "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
        #     ])
        # cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.A_back_url = conf.get('DEFAULT', 'A_back_url')
        # 获取明天日期
        cls.end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        cls.group_id = None

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Coupons_el = Coupons_el(self.driver, Keys)
        # self.Airtest_Server = Airtest_Server(self.poco, api)
        # self.Req_login = Req_login(requests)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.A_back_url + data['el_login_backpath']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/coupons.yaml')
    def test_1(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 新建优惠卷
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])

    @file_data('../Data/grant_coupons.yaml')
    def test_2(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 发放优惠卷
        grant_coupons = self.util.str_by_tuple(kwargs['grant_coupons'])
        Element_data = kwargs['Element_data']
        Element_data['end_dates'] = self.end_dates
        # 优惠卷列表表单
        coupons_lis = self.util.str_by_tuple(kwargs['coupons_lis'])
        # 业务实现
        self.Login_case.menu_module(menu_path=menu_path, again_menu=kwargs['Element_data'])
        self.Coupons_el.grant_coupons(coupons_el=grant_coupons, element_data=kwargs['Element_data'],
                                      coupons_lis=coupons_lis)
        # 断言
        grant_text = self.Coupons_el.grant_text
        coupons_key = self.Coupons_el.coupons_key
        self.assertEqual(first=grant_text, second=coupons_key, msg='优惠卷发放失败')

    def test_5_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
