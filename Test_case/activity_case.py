import unittest
from selenium import webdriver
from Page.activity import *
from selenium.webdriver.common.keys import Keys
from ddt import ddt, file_data
from Page.Login import *


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
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/activity.yaml')
    def test_1_newgroup(self, **kwargs):
        """新建拼团活动"""
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        activitys_menu = self.str_by_tuple(activitys['activitys_menu'])
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = self.str_by_tuple(grouds['grouds_goods'])
        new_groud = self.str_by_tuple(grouds['new_groud'])
        new_data = grouds['new_data']
        self.activity_case.new_groud(activitys_el=activitys_menu, groud_el=grouds_goods, group_data=new_data,
                                     newgroud_el=new_groud)
        self.new_textone = self.activity_case.new_textone
        self.new_texttwo = self.activity_case.new_texttwo
        self.assertEqual(first=self.new_textone, second=self.new_texttwo, msg='新建拼团失败！')

    # def test_2_addgroup(self, **kwargs):
    #     pass

    @file_data('../Data/activity.yaml')
    def test_2_deletegroup(self, **kwargs):
        """删除拼团"""
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = self.str_by_tuple(grouds['grouds_goods'])
        self.activity_case.delete_group(groud_el=grouds_goods)
        self.delete_text = self.activity_case.delete_text
        self.assertEqual(first='true', second=self.activity_case.delete_text, msg='删除拼团失败！')

    def test_3_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
