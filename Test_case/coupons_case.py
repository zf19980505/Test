import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import configparser
import datetime
from ddt import ddt, file_data
from Page.Login import *


@ddt
class Coupons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.A_back_url = conf.get('DEFAULT', 'A_back_url')

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.str_by_tuple(kwargs['login'])
        url = self.A_back_url + data['el_login_backpath']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 拿到小程序token并且赋值方便后面使用
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/coupons.yaml')
    def test_1_newcoupons(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 优惠卷列表
        coupons = self.util.str_by_tuple(kwargs['coupons_lis'])
        # 新建优惠卷
        new_coupons = self.util.str_by_tuple(kwargs['new_coupons'])
        Element_data = kwargs['Element_data']
        # 获取明天日期
        end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        Element_data['end_dates'] = end_dates
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.new_groud(element_data=Element_data, coupons=coupons,
                                     new_coupons=new_coupons)

    def test_5_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
