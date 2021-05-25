import unittest
from selenium import webdriver
from Page.activity import *
from ddt import ddt, file_data
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# import BeautifulReport


@ddt
class Activity_TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.activity_case = Activity(self.driver)

    @file_data('../Data/activity.yaml')
    def test_new_group(self, **kwargs):
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
        new_textone = self.activity_case.new_textone
        new_texttwo = self.activity_case.new_texttwo
        self.assertEqual(first=new_textone, second=new_texttwo, msg='新建拼团失败')

    @file_data('../Data/activity.yaml')
    def test_delete_group(self, **kwargs):
        """删除拼团"""
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = grouds['grouds_goods']
        self.activity_case.delete_group(groud_el=grouds_goods)

    # def tearDown(self):
    #     test_text = self.activity_case.login_text
    #     self.assertEqual(first=self.data['verify'], second=test_text, msg='访问首页有误')


if __name__ == '__main__':
    unittest.TestCase()
    # test_case = unittest.TestLoader().loadTestsFromTestCase(TestRun)
    # BeautifulReport.BeautifulReport(
    #   test_case).report(filename='login_report', description='登录自动化', report_dir='../Report')
