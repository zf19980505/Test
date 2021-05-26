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

    @file_data('../Data/login.yaml')
    def test_0_loging(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        date = kwargs['login']
        self.Login_case.logins(username=data['username'], password=data['password'], url=data['url'], elemter=date)
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/activity.yaml')
    def test_1_newgroup(self, **kwargs):
        """新建拼团活动"""
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = grouds['grouds_goods']
        new_groud = grouds['new_groud']
        new_data = grouds['new_data']
        self.activity_case.new_groud(activitys_el=activitys, groud_el=grouds_goods, group_data=new_data,
                                     newgroud_el=new_groud)
        self.new_textone = self.activity_case.new_textone
        self.new_texttwo = self.activity_case.new_texttwo
        self.assertEqual(first=self.new_textone, second=self.new_texttwo, msg='新建拼团失败！')

    @file_data('../Data/activity.yaml')
    def test_2_deletegroup(self, **kwargs):
        """删除拼团"""
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = grouds['grouds_goods']
        self.activity_case.delete_group(groud_el=grouds_goods)
        self.delete_text = self.activity_case.delete_text
        self.assertEqual(first='true', second=self.activity_case.delete_text, msg='删除拼团失败！')

    def test_3_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()