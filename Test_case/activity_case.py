import unittest
from selenium import webdriver
from Page.activity import *
from Page.Login import *
from selenium.webdriver.common.keys import Keys
from ddt import ddt, file_data


# import BeautifulReport


@ddt
class Activity_TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.activity_case = Activity(self.driver, Keys)

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

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        login_el = self.str_by_tuple(kwargs['login'])
        self.Login_case.logins(username=data['username'], password=data['password'], url=data['url'], elemter=login_el)
        # 断言校验
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

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
        self.activity_case.new_groud(menu_path=menu_path, element_data=kwargs['Element_data'], group=group,
                                     new_group=new_group)
        # 断言校验
        self.new_textone = self.activity_case.new_textone
        self.new_texttwo = self.activity_case.new_texttwo
        self.assertEqual(first=self.new_textone, second=self.new_texttwo, msg='新建拼团失败！')

    @file_data('../Data/Goodsarea.yaml')
    def test_2_add_areagoods(self, **kwargs):
        menu_path = self.str_by_tuple(kwargs['menu_path'])
        goods_area = self.str_by_tuple(kwargs['goods_area'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.add_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
        # 断言校验
        add_goods_text = self.activity_case.add_goods_text
        self.assertEqual(first='True', second=add_goods_text, msg='拼团商品添加布局失败')

    @file_data('../Data/activity.yaml')
    def test_3_deletegroup(self, **kwargs):
        """删除拼团"""
        # 首页菜单
        menu_path = self.str_by_tuple(kwargs['menu_path'])
        # 拼团
        group = self.str_by_tuple(kwargs['group'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.delete_group(groud_el=group)
        # 断言校验
        self.delete_text = self.activity_case.delete_text
        self.assertEqual(first='true', second=self.activity_case.delete_text, msg='删除拼团失败！')

    @file_data('../Data/Goodsarea.yaml')
    def test_4_deleter_areagoods(self, **kwargs):
        menu_path = self.str_by_tuple(kwargs['menu_path'])
        goods_area = self.str_by_tuple(kwargs['goods_area'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.activity_case.deleter_area_group(goods_area=goods_area, element_data=kwargs['Element_data'])
        # 断言校验
        delete_goods_text = self.activity_case.delete_goods_text
        self.assertEqual(first='True', second=delete_goods_text, msg='从布局里删除拼团商品失败')

    def test_5_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
