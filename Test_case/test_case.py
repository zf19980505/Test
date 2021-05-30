import unittest
from selenium import webdriver
from Page.test import *
from Page.Login import *
from selenium.webdriver.common.keys import Keys
from ddt import ddt, file_data


@ddt
class test_TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)
        self.Test_case = Test(self.driver, Keys)

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

    @file_data('../Data/Goodsarea.yaml')
    def delete_area(self, **kwargs):
        menu_path = self.str_by_tuple(kwargs['menu_path'])
        goods_area = self.str_by_tuple(kwargs['goods_area'])
        self.Login_case.menu_module(menu_path=menu_path, element_data=kwargs['Element_data'])
        self.Test_case.add_group(goods_area=goods_area, element_data=kwargs['Element_data'])
        # 断言校验
        add_goods_text = self.Test_case.add_goods_text
        self.assertEqual(first='True', second=add_goods_text, msg='拼团商品添加布局失败')

    def test_4_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()