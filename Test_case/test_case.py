from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import unittest
from Page.test import *
from ddt import ddt, file_data


@ddt
class Air_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not cli_setup():
            cls.driver = auto_setup(__file__, logdir=True, devices=[
                "Android://127.0.0.1:5037/43793282?cap_method=JAVACAP^&^&ori_method=ADBORI",
            ])
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    def setUp(self):
        self.air_case = Airtest_Server(self.poco)

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

    @file_data('../Data/Test.yaml')
    def test_weixin(self, **kwargs):
        size = self.str_szie(kwargs['swipe'])
        self.air_case.test_wx(air_el=kwargs['weixin'], air_data=size)


if __name__ == '__main__':
    unittest.main()
