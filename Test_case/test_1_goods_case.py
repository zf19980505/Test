import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
from Page.goods import *
from Page.Login import *
from ddt import ddt, file_data
from Util.data_conversion import *
import configparser
# import BeautifulReport


@ddt
class Goods_TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        # 万色城二期总部后台
        cls.wsc_admin_url = conf.get('DEFAULT', 'wsc_admin_url')
        # 万色城二期分销后台
        cls.wsc_back_url = conf.get('DEFAULT', 'wsc_back_url')
        cls.util = Data_conversion()
        cls.driver = webdriver.Chrome()
        cls.admin = None
        cls.back = None
        cls.master_map = None

    def setUp(self):
        self.Login_case = Login_server(driver=self.driver)
        self.goods_case = Goods(driver=self.driver, keyboard=Keys, action=ActionChains)
        self.Req_goods = Req_goods(requests)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_admin_url + data['el_login_path']
        url2 = self.wsc_back_url + data['el_login_backpath']
        Goods_TestRun.admin, Goods_TestRun.back = self.Login_case.logins(username=data['username'],
                                                                         password=data['password'], url=url, url2=url2,
                                                                         elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        login2_text = self.Login_case.login2_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问总部首页有误')
        self.assertEqual(first=data['verify'], second=login2_text, msg='访问分销首页有误')

    @file_data('../Data/goods.yaml')
    def test_1_upload_goods(self, **kwargs):
        """"上传商品"""
        # 数据处理
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        goods_el = self.util.str_by_tuple(kwargs['goods_spu'])
        goods_data = kwargs['Element_data']
        goods_data['goods_spu'] = self.util.read_xls(goods_data['goods_spu_ex'])
        # 业务
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        new_goods_text = self.goods_case.upload_goods(elemter=goods_el, goods_data=goods_data)
        # 断言
        self.assertEqual(first=True, second=new_goods_text, msg='上传模板商品失败')

    @file_data('../Data/goods.yaml')
    def test_2_edit_goodsmap(self, **kwargs):
        # 数据处理
        goods_el = self.util.str_by_tuple(kwargs['goods_spu'])
        req_goods = kwargs['Req_goods']
        req_path = req_goods['path']
        req_data = req_goods['data']
        url = self.wsc_admin_url + req_path['look_spu_path']
        # 业务
        Goods_TestRun.master_map = self.Req_goods.look_goods(url=url, params=req_data)
        if self.master_map is not None:
            self.goods_case.edit_goods(elemter=goods_el, goods_data=kwargs['Element_data'])
            assert_map = self.Req_goods.look_goods(url=url, params=req_data)
            if self.master_map != assert_map:
                self.master_map = True
            else:
                self.master_map = False
        # 断言
        self.assertEqual(first=True, second=self.master_map, msg='给旺店通拉取商品编辑图片失败')

    @file_data('../Data/goods.yaml')
    def test_3_up_goods(self, **kwargs):
        # 数据处理
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        goods_el = self.util.str_by_tuple(kwargs['goods_spu'])
        goods_data = kwargs['Element_data']
        goods_data['goods_spu'] = self.util.read_xls(goods_data['goods_spu_ex'])
        goods_data['back'] = self.back
        goods_data['admin'] = self.admin
        # 业务
        # 总部
        admin_up_goods = self.goods_case.up_down_goods(elemter=goods_el, goods_data=goods_data)
        # 分销
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        up_goods = self.goods_case.up_down_goods(elemter=goods_el, goods_data=goods_data, page=admin_up_goods)
        # 断言
        self.assertEqual(first=True, second=up_goods, msg='上架商品在分销后台看不到')

    def test_4_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
    # test_case = unittest.TestLoader().loadTestsFromTestCase(TestRun)
    # BeautifulReport.BeautifulReport(
    #   test_case).report(filename='login_report', description='登录自动化', report_dir='../Report')
