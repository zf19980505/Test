import unittest
from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
from Page.Login import *
from Page.Layout import *
from ddt import ddt, file_data
from Util.data_conversion import *
import configparser


@ddt
class LayoutCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        yeshen = conf.get('DEFAULT', 'air_yeshen')
        if not cli_setup():
            api.auto_setup(__file__, logdir=None, devices=[yeshen])
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # 万色城二期总部后台
        cls.wsc_admin_url = conf.get('DEFAULT', 'wsc_admin_url')
        # 万色城二期分销后台
        cls.wsc_back_url = conf.get('DEFAULT', 'wsc_back_url')
        cls.util = Data_conversion()
        cls.driver = webdriver.Chrome()
        cls.admin = None
        cls.back = None
        # 一排一的布局编码
        cls.one_area_coding = None

    def setUp(self):
        self.Login_case = Login_server(driver=self.driver)
        self.LayoutPage = LayoutPage(driver=self.driver)
        self.LayoutAir = LayoutAir(self.poco, api)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录 """
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_admin_url + data['el_login_path']
        url2 = self.wsc_back_url + data['el_login_backpath']
        LayoutCase.admin, LayoutCase.back = self.Login_case.logins(username=data['username'],
                                                                   password=data['password'], url=url, url2=url2,
                                                                   elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        login2_text = self.Login_case.login2_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问总部首页有误')
        self.assertEqual(first=data['verify'], second=login2_text, msg='访问分销首页有误')

    @file_data('../Data/Layout.yaml')
    def test_1_new_home_layout(self, **kwargs):
        # 数据处理
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        public_layout = self.util.str_by_tuple(kwargs['public_layout'])
        new_layout = self.util.str_by_tuple(kwargs['new_layout'])
        element_data = kwargs['Element_data']
        element_data['back'] = self.back
        element_data['admin'] = self.admin
        # 业务处理
        # 总部后台
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        layout_result = self.LayoutPage.new_home_layout(layout_el=new_layout, layout_data=element_data,
                                                        public_el=public_layout)
        if layout_result:
            # 分销后台
            self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
            result = self.LayoutPage.new_home_layout(layout_el=new_layout, layout_data=element_data, page=layout_result,
                                                     public_el=public_layout)
            if result:
                air_result = self.LayoutAir.xcx_look_homelayout(air_el=kwargs['air_layout'], air_data=element_data)
                self.assertEqual(first=True, second=air_result, msg='总部分销新建板块成功，小程序未显示')
            else:
                self.assertEqual(first=True, second=result, msg='总部新建首页板块成功并开启后分销后台未显示')
        else:
            self.assertEqual(first=True, second=layout_result, msg='新建首页板块失败')

    @file_data('../Data/goods_area.yaml')
    def test_2_new_goods_area(self, **kwargs):
        # 数据处理
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        public_area = self.util.str_by_tuple(kwargs['public_area'])
        new_goods_area = self.util.str_by_tuple(kwargs['new_goods_area'])
        element_data = kwargs['Element_data']
        element_data['back'] = self.back
        element_data['admin'] = self.admin
        # 业务处理
        # 总部后台
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        LayoutCase.one_area_coding = self.LayoutPage.new_goods_area(area_el=new_goods_area, area_data=element_data,
                                                                    public_el=public_area)
        if self.one_area_coding:
            self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
            result = self.LayoutPage.new_goods_area(area_el=new_goods_area, area_data=element_data,
                                                    page=self.one_area_coding, public_el=public_area)
            self.assertEqual(first=True, second=result, msg='总部新建商品板块成功后分销后台看不到')
        else:
            self.assertEqual(first=True, second=self.one_area_coding, msg='新建商品板块失败')

    def test_3_area_join_layout(self, **kwargs):
        pass

    def test_4_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.TestCase()