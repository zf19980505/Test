import unittest
from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
from Page.activity import *
from Page.Login import *
from selenium.webdriver.common.keys import Keys
import requests
import configparser
from ddt import ddt, file_data


# import BeautifulReport


@ddt
class Activity_TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # if not cli_setup():
        #     cls.driver = api.auto_setup(__file__, logdir=None, devices=[
        #         "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
        #     ])
        # cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        cls.driver = webdriver.Chrome()
        conf = configparser.ConfigParser()
        conf.read('../Confing/request_confing.ini')
        cls.url = conf.get('DEFAULT', 'url')
        # 定义一个参数接收储存添加成为拼团商品的SPU
        cls.group_good_spu = None
        # 定义一个参数接收储存添加成为拼团商品的ID
        # cls.group_id = None

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Req_login = Req_login(requests)
        self.activity_case = Activity(self.driver, Keys)
        # self.air_activity = Air_Activity(self.poco, api)
        self.Req_Activity = Req_Activity(requests)

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

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.str_by_tuple(kwargs['login'])
        url = self.url + data['el_login_path']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')\

    @file_data('../Data/activity.yaml')
    def test_1_newgroup(self, **kwargs):
        """新建拼团活动"""
        # 首页菜单
        menu_path = self.str_by_tuple(kwargs['menu_path'])
        # 拼团
        group = self.str_by_tuple(kwargs['group'])
        # 新建拼团活动
        new_group = self.str_by_tuple(kwargs['new_group'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.new_groud(element_data=kwargs['Element_data'], group=group,
                                     new_group=new_group)
        # 断言校验
        new_textone = self.activity_case.new_textone
        Activity_TestRun.group_good_spu = self.activity_case.new_texttwo
        self.assertEqual(first=new_textone, second=self.group_good_spu, msg='新建拼团失败！')

    @file_data('../Data/Test.yaml')
    def test_2_xcxgroup(self, **kwargs):
        size = self.str_szie(kwargs['swipe'])
        xcx_el_data = kwargs['xcx_el_data']
        self.air_activity.xcx_group(air_el=kwargs['weixin'], air_swipe=size, air_data=xcx_el_data)
        # 断言校验
        xcx_group_text = self.air_activity.xcx_group_text
        self.assertEqual(first='True', second=xcx_group_text, msg='该商品不是拼团商品')

    # @file_data('../Data/Goodsarea.yaml')
    # def test_2_add_areagoods(self, **kwargs):
    #     menu_path = self.str_by_tuple(kwargs['menu_path'])
    #     goods_area = self.str_by_tuple(kwargs['goods_area'])
    #     self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
    #     self.activity_case.add_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
    #     # 断言校验
    #     add_goods_text = self.activity_case.add_goods_text
    #     self.assertEqual(first='True', second=add_goods_text, msg='拼团商品添加布局失败')

    @file_data('../Data/activity.yaml')
    def test_3_deletegroup(self, **kwargs):
        """删除拼团"""
        # todo 接口删除
        req_grouop = kwargs['req_grouop']
        path = req_grouop['path']
        data = req_grouop['data']
        data['public_data']['spucode'] = self.group_good_spu
        url = self.url + path['gruop_goods_lis_path']
        delete_url = self.url + path['delete_group_path']
        self.Req_Activity.gruop_goods_lis(url=url, params=data['gruop_goods_lis_data'], public_data=data['public_data'])
        req_grouop['data']['delte_group_data'] = {'id': self.Req_Activity.group_id}
        self.Req_Activity.delete_group_good(url=delete_url, params=data['delte_group_data'])
        delete_text = self.Req_Activity.delete_text
        self.assertEqual(first='True', second=delete_text, msg='拼团删除失败，服务器报错')
        # todo UI页面删除删除
        # 拼团
        # group = self.str_by_tuple(kwargs['group'])
        # self.activity_case.delete_group(groud_el=group)
        # # 断言校验
        # self.delete_text = self.activity_case.delete_text
        # self.assertEqual(first='true', second=self.activity_case.delete_text, msg='删除拼团失败！')

    # @file_data('../Data/Goodsarea.yaml')
    # def test_4_deleter_areagoods(self, **kwargs):
    #     menu_path = self.str_by_tuple(kwargs['menu_path'])
    #     goods_area = self.str_by_tuple(kwargs['goods_area'])
    #     self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
    #     self.activity_case.deleter_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
    #     # 断言校验
    #     delete_goods_text = self.activity_case.delete_goods_text
    #     self.assertEqual(first='True', second=delete_goods_text, msg='从布局里删除拼团商品失败')

    def test_5_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
