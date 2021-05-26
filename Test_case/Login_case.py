import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from airtest.core.api import *
# from airtest.cli.parser import cli_setup
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Page.Login import *
from ddt import ddt, file_data


@ddt
class Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        # if not cli_setup():
        #     cls.driver = auto_setup(__file__, logdir=True, devices=[
        #         "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
        #     ])
        # cls.test_poco = Airtest_Server(AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False))

    def setUp(self):
        self.Login_case = Login_server(self.driver, Keys)

    @file_data('../Data/login.yaml')
    def test_open(self, **kwargs):
        """"登录"""
        data = kwargs['data']
        date = kwargs['login']
        self.Login_case.logins(username=data['username'], password=data['password'], url=data['url'], elemter=date)
        test_text = self.Login_case.login_text
        self.assertEqual(first=data['verify'], second=test_text, msg='访问首页有误')

    def test_over(self):
        self.Login_case.close()


if __name__ == '__main__':
    unittest.main()
