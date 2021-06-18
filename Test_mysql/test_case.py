from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
import unittest
from Page.test import *
from Page.Login import *
from Page.Coupons import *
from Page.goods import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
import configparser
from ddt import ddt, file_data
from Util.data_conversion import *
import datetime


@ddt
class Air_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.util = Data_conversion()
        cls.driver = webdriver.Chrome()
        # yeshen = conf.get('DEFAULT', 'air_yeshen')
        # if not cli_setup():
        #     api.auto_setup(__file__, logdir=None, devices=[yeshen])
        # cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # 万色城二期总部后台
        cls.wsc_admin_url = conf.get('DEFAULT', 'wsc_admin_url')
        # 万色城二期分销后台
        cls.wsc_back_url = conf.get('DEFAULT', 'wsc_back_url')
        # # 万色城二期小程序
        # cls.wsc_xcx_back = conf.get('DEFAULT', 'wsc_xcx_back')
        # # 获取后天日期
        # cls.end_two_dates = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        # # 获取明天日期
        # cls.end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # cls.group_id = None
        cls.master_map = None

    def setUp(self):
        self.Login_case = Login_server(self.driver)
        self.goods_case = Goods(driver=self.driver, action=ActionChains)
        self.Req_goods = Req_goods(requests)
        # self.Coupons_el = Coupons_el(self.driver, Keys)
        # self.Req_coupons = Req_coupons(requests)
        # self.Air_coupons = Air_coupons(self.poco, api)
        # self.Airtest_Server = Airtest_Server(self.poco, api)
        # self.Req_login = Req_login(requests)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_admin_url + data['el_login_path']
        # url = self.wsc_back_url + data['el_login_backpath']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    # @file_data('../Data/goods.yaml')
    # def test_1(self, **kwargs):
    #     # 数据处理
    #     menu_path = self.util.str_by_tuple(kwargs['menu_path'])
    #     goods_el = self.util.str_by_tuple(kwargs['goods_spu'])
    #     req_goods = kwargs['Req_goods']
    #     req_path = req_goods['path']
    #     req_data = req_goods['data']
    #     url = self.wsc_admin_url + req_path['look_spu_path']
    #     # 业务
    #     self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
    #     Air_test.master_map = self.Req_goods.look_goods(url=url, params=req_data)
    #     if self.master_map is not None:
    #         self.goods_case.edit_goods(elemter=goods_el, goods_data=kwargs['Element_data'])
    #         assert_map = self.Req_goods.look_goods(url=url, params=req_data)
    #         if self.master_map != assert_map:
    #             self.master_map = True
    #         else:
    #             self.master_map = False
    #     # 断言
    #     self.assertEqual(first=True, second=self.master_map, msg='给旺店通拉取商品编辑图片失败')

    # @file_data('../Data/coupon_envelope.yaml')
    # def test_2(self, **kwargs):
    #     air_envelope = kwargs['Air_envelope']
    #     print(air_envelope['xcx_return'])

    def test_5_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
