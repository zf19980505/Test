import unittest
from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Page.activity import *
from Page.Login import *
from Util.data_conversion import *
import requests
import configparser
from ddt import ddt, file_data


# import BeautifulReport


@ddt
class Activity_TestRun(unittest.TestCase):
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
        # 定义一个参数接收储存添加成为拼团商品的SPU
        cls.group_good_spu = None
        # 定义一个参数接收储存添加成为拼团商品的ID
        cls.group_id = None

    def setUp(self):
        self.Login_case = Login_server(driver=self.driver)
        self.activity_case = Activity(driver=self.driver, keyboard=Keys)
        self.air_activity = Air_Activity(self.poco, api)
        self.Req_Activity = Req_Activity(requests)

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_admin_url + data['el_login_path']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/activity.yaml')
    def test_1_newgroup(self, **kwargs):
        """新建拼团活动"""
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 拼团
        group = self.util.str_by_tuple(kwargs['group'])
        # 新建拼团活动
        new_group = self.util.str_by_tuple(kwargs['new_group'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.new_groud(element_data=kwargs['Element_data'], group=group,
                                     new_group=new_group)
        # 断言校验
        new_textone = self.activity_case.new_textone
        Activity_TestRun.group_good_spu = self.activity_case.new_texttwo
        self.assertEqual(first=new_textone, second=self.group_good_spu, msg='新建拼团失败！')

    @file_data('../Data/xcx_group.yaml')
    def test_2_xcxgroup(self, **kwargs):
        size = self.util.str_lis(kwargs['swipe'])
        xcx_group_text = self.air_activity.xcx_group(air_el=kwargs['xcx'], air_swipe=size, air_data=kwargs['xcx_el_data'])
        # 断言校验
        self.assertEqual(first=True, second=xcx_group_text, msg='该商品不是拼团商品')

    # todo 把拼团商品添加进入商品布局管理
    # @file_data('../Data/Goodsarea.yaml')
    # def test_2_add_areagoods(self, **kwargs):
    #     menu_path = self.util.str_by_tuple(kwargs['menu_path'])
    #     goods_area = self.util.str_by_tuple(kwargs['goods_area'])
    #     self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
    #     self.activity_case.add_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
    #     # 断言校验
    #     add_goods_text = self.activity_case.add_goods_text
    #     self.assertEqual(first='True', second=add_goods_text, msg='拼团商品添加布局失败')

    @file_data('../Data/activity.yaml')
    def test_3_deletegroup(self, **kwargs):
        """删除拼团"""
        # todo 接口直接请求删除
        req_grouop = kwargs['req_grouop']
        path = req_grouop['path']
        data = req_grouop['data']
        data['public_data']['spucode'] = self.group_good_spu
        url = self.wsc_admin_url + path['gruop_goods_lis_path']
        delete_url = self.wsc_admin_url + path['delete_group_path']
        self.Req_Activity.gruop_goods_lis(url=url, params=data['gruop_goods_lis_data'], public_data=data['public_data'])
        req_grouop['data']['delte_group_data'] = {'id': self.Req_Activity.group_id}
        self.Req_Activity.delete_group_good(url=delete_url, params=data['delte_group_data'])
        delete_text = self.Req_Activity.delete_text
        self.assertEqual(first='True', second=delete_text, msg='拼团删除失败，服务器报错')
        # todo UI页面点击删除按钮删除
        # 拼团
        # group = self..str_by_tuple(kwargs['group'])
        # self.activity_case.delete_group(groud_el=group)
        # # 断言校验
        # self.delete_text = self.activity_case.delete_text
        # self.assertEqual(first='true', second=self.activity_case.delete_text, msg='删除拼团失败！')

    # todo 把拼团商品从商品布局管理里删除
    # @file_data('../Data/Goodsarea.yaml')
    # def test_4_deleter_areagoods(self, **kwargs):
    #     menu_path = self.util.str_by_tuple(kwargs['menu_path'])
    #     goods_area = self.util.str_by_tuple(kwargs['goods_area'])
    #     self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
    #     self.activity_case.deleter_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
    #     # 断言校验
    #     delete_goods_text = self.activity_case.delete_goods_text
    #     self.assertEqual(first='True', second=delete_goods_text, msg='从布局里删除拼团商品失败')

    def test_4_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
