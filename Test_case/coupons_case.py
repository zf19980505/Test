import unittest
from airtest.cli.parser import cli_setup
from airtest.core import api
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import configparser
import datetime
from ddt import ddt, file_data
from Util.data_conversion import *
from Page.Login import *
from Page.Coupons import *


@ddt
class Coupons(unittest.TestCase):
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
        # 万色城二期分销后台
        cls.wsc_back_url = conf.get('DEFAULT', 'wsc_back_url')
        # 万色城二期小程序
        cls.wsc_xcx_back = conf.get('DEFAULT', 'wsc_xcx_back')
        # 获取后天日期
        cls.end_two_dates = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        # 获取明天日期
        cls.end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        cls.coupons_key = None
        cls.coupons_name = None

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Coupons_el = Coupons_el(self.driver, Keys)
        self.Req_coupons = Req_coupons(requests)
        self.Air_coupons = Air_coupons(self.poco, api)

    # todo 登录
    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.util.str_by_tuple(kwargs['login'])
        url = self.wsc_back_url + data['el_login_backpath']
        self.Login_case.logins(username=data['username'], password=data['password'], url=url, elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    # todo 新建优惠卷
    @file_data('../Data/coupons.yaml')
    def test_1_newcoupons(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 新建优惠卷
        new_coupons = self.util.str_by_tuple(kwargs['new_coupons'])
        Element_data = kwargs['Element_data']
        Element_data['end_dates'] = self.end_two_dates
        # 优惠卷列表表单
        coupons_lis = self.util.str_by_tuple(kwargs['coupons_lis'])
        # 业务实现
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.Coupons_el.new_coupons(element_data=Element_data, new_coupons=new_coupons, coupons_lis=coupons_lis)
        # 断言
        Coupons.coupons_name = self.Coupons_el.coupons_name
        self.assertEqual(first=Element_data['coupons_name'], second=self.coupons_name, msg='新建优惠卷失败')

    # todo 新建开屏红包
    @file_data('../Data/coupon_envelope.yaml')
    def test_2_couponenvelope(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 新建开屏红包
        new_envelope = self.util.str_by_tuple(kwargs['new_envelope'])
        # 优惠卷列表表单
        envelope_lis = self.util.str_by_tuple(kwargs['envelope_lis'])
        element_data = kwargs['Element_data']
        element_data['end_dates'] = self.end_dates
        self.Login_case.menu_module(menu_path=menu_path, again_menu=kwargs['Element_data'])
        self.Coupons_el.new_coupon_envelope(envelope_el=new_envelope, element_data=element_data,
                                            envelope_lis=envelope_lis)
        # 断言
        envelope_text = self.Coupons_el.envelope_text
        self.assertEqual(first=element_data['envelope_name'], second=envelope_text, msg='新建开屏红包失败')

    # todo 发放优惠卷
    @file_data('../Data/grant_coupons.yaml')
    def test_3_grantcoupons(self, **kwargs):
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
        Coupons.coupons_key = self.Coupons_el.coupons_key
        self.assertEqual(first=grant_text, second=self.coupons_key, msg='优惠卷发放失败')

    # todo 用户小程序查看优惠卷
    @file_data('../Data/grant_coupons.yaml')
    def test_4_xcx_couponscentre(self, **kwargs):
        size = self.util.str_lis(kwargs['swipe'])
        Air_coup = kwargs['Air_coup']
        Air_coup['coupons_name'] = {'text': self.coupons_name}
        self.Air_coupons.look_grant_coupons(air_el=Air_coup, air_swipe=size, air_data=kwargs['Element_data'])
        # 断言
        self.assertEqual(first=True, second=self.Air_coupons.air_grant_coupons_text, msg='小程序页面上看不到该优惠券')

    # todo 小程序查看开屏红包并领取开屏红包
    @file_data('../Data/coupon_envelope.yaml')
    def test_5_xcx_lookenvelope(self, **kwargs):
        size = self.util.str_lis(kwargs['swipe'])
        air_envelope = kwargs['Air_envelope']
        self.Air_coupons.look_coupon_envelope(air_el=kwargs['Air_envelope'], air_data=kwargs['Element_data'])
        # 断言
        if not self.Air_coupons.look_envelope_text:
            self.assertEqual(first=True, second=self.Air_coupons.look_envelope_text, msg='小程序上未展示开屏红包')
        else:
            air_envelope['coupons_name'] = {'text': self.coupons_name}
            self.Air_coupons.look_grant_coupons(air_el=air_envelope, air_swipe=size, air_data=kwargs['Element_data'])
            self.assertEqual(first=True, second=self.Air_coupons.air_grant_coupons_text, msg='点击了开屏红包但是并未领取到')

    # todo 我的优惠券查看领取到的优惠券
    @file_data('../Data/grant_coupons.yaml')
    def test_6_xcx_Mycoup(self, **kwargs):
        size = self.util.str_lis(kwargs['swipe'])
        coupons_sql = kwargs['Mysql']
        Air_Mycoup = kwargs['Air_Mycoup']
        Air_Mycoup['coupons_name'] = {'text': self.coupons_name}
        self.Air_coupons.look_grant_coupons(air_el=Air_Mycoup, air_swipe=size, air_data=kwargs['Element_data'])
        # 断言
        if self.Air_coupons.air_grant_coupons_text:
            mysql = Mysql_coupons(coupons_sql['sql_name'])
            mysql.delete_my_coupons(sql_el=coupons_sql)
            if not mysql.delete_mycoupons_text:
                self.assertEqual(first=True, second=mysql.delete_mycoupons_text, msg='数据库语句删除失败')
        else:
            self.assertEqual(first=True, second=self.Air_coupons.air_grant_coupons_text, msg='小程序我的优惠券上看不到刚领取的优惠券')

    # @file_data('../Data/grant_coupons.yaml')
    # def test_4_look_coupons(self, **kwargs):
    #     xcx_coupons = kwargs['xcx_coupons']
    #     xcx_coupons['coupons_key'] = self.coupons_key
    #     url = self.wsc_xcx_back + xcx_coupons['get_coupons_path']
    #     self.Req_coupons.xcx_look_coupons(url=url, params=xcx_coupons['look_coupons_data'],
    #                                       headers=xcx_coupons['headers'], public_data=xcx_coupons)
    #     # 断言
    #     get_coupons_text = self.Req_coupons.get_coupons_text
    #     self.assertEqual(first=self.coupons_key, second=get_coupons_text, msg='小程序接口找不到该优惠卷')

    # todo 接口直接领取优惠券
    @file_data('../Data/grant_coupons.yaml')
    def test_7_get_coupons(self, **kwargs):
        xcx_coupons = kwargs['xcx_coupons']
        xcx_coupons['coupons_key'] = self.coupons_key
        url = self.wsc_xcx_back + xcx_coupons['get_coupons_path']
        xcx_coupons['get_coupons_data'] = {'coupon_node_id': self.coupons_key}
        self.Req_coupons.xcx_get_coupons(url=url, data=xcx_coupons['get_coupons_data'], headers=xcx_coupons['headers'])
        # 断言
        get_coupons_text = self.Req_coupons.get_coupons_text
        self.assertEqual(first='True', second=get_coupons_text, msg='用户领取优惠卷失败')

    # todo 删除优惠卷
    @file_data('../Data/delete_coupon.yaml')
    def test_8_delete_coupons(self, **kwargs):
        # 首页菜单
        menu_path = self.util.str_by_tuple(kwargs['menu_path'])
        # 拿到之前存起来的key值
        kwargs['Element_data']['coupons_key'] = self.coupons_key
        kwargs['Element_data']['coupons_name'] = self.coupons_name
        # 优惠券列表页
        coupons_lis = self.util.str_by_tuple(kwargs['coupons_lis'])
        # Air小程序数据
        size = self.util.str_lis(kwargs['swipe'])
        air_coup = kwargs['Air_coup']
        air_coup['coupons_name'] = {'text': self.coupons_name}
        # 通过连接数据库执行删除语句删除刚刚领取优惠卷的用户记录
        coupons_sql = kwargs['Mysql']
        mysql = Mysql_coupons(coupons_sql['sql_name'])
        mysql.delete_my_coupons(sql_el=coupons_sql)
        if not mysql.delete_mycoupons_text:
            self.assertEqual(first=True, second=mysql.delete_mycoupons_text, msg='数据库语句删除失败')
            pass
        # 重新回到优惠劵列表页面
        self.Login_case.menu_module(menu_path=menu_path, again_menu=kwargs['Element_data'])
        self.Coupons_el.delete_coupon(coupon_el=coupons_lis, element_data=kwargs['Element_data'])
        # 断言
        if self.Coupons_el.delete_coupon_text is True:
            self.Air_coupons.look_grant_coupons(air_el=air_coup, air_swipe=size, air_data=kwargs['Element_data'])
            self.assertEqual(first=False, second=self.Air_coupons.air_grant_coupons_text, msg='删除了的优惠券在小程序上还存在')
        else:
            self.assertEqual(first=True, second=self.Coupons_el.delete_coupon_text, msg='后台分销的优惠券删除失败')

    def test_9_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()