from selenium import webdriver
from appium import webdriver as apiwebdriver
from ddt import ddt, file_data
from time import sleep
from Page.activity import *
import unittest


@ddt
class Testapi(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            "platformName": "Android",
            "deviceName": "43793202",
            "platformVersion": "9",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            "noReset": "true"
        }
        self.api_casss = Apiactivity(apiwebdriver, desired_caps)

    @file_data('../Data/Apilogin.yaml')
    def test_api(self, **kwargs):
        self.api_casss.test_api(api_el=kwargs['mimiapp'])


if __name__ == '__main__':
    unittest.TestCase()
