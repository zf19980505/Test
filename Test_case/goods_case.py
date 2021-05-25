import unittest
from selenium import webdriver
from Page.goods import *
from ddt import ddt, file_data
# import BeautifulReport

driver = webdriver.Chrome()


@ddt
class Goods_TestRun(unittest.TestCase):
    # def __init__(self, *args, **kwargs):
    #     super(TestRun, self).__init__(*args, **kwargs)
    #     self.

    def setUp(self):
        self.goods_case = Goods(driver)
    #
    # @file_data('../Data/login.yaml')
    # def test_login(self, **kwargs):
    #     """"登录"""
    #     data = kwargs['data']
    #     date = kwargs['login']
    #     self.goods_case.login(username=data['username'], password=data['password'], url=data['url'], elemter=date)
    #     test_text = self.goods_case.login_text
    #     self.assertEqual(first=self.data['verify'], second=test_text, msg='访问首页有误')

    @file_data('../Data/goods.yaml')
    def test_upload_goods(self, **kwargs):
        """"上传商品"""
        date = kwargs['goods_spu']
        self.goods_case.upload_goods(elemter=date, goods_spu_ex=date['goods_spu_ex'])
        # test_text = self.goods_case.goods_spu_text
        # self.assertEqual(first=date['goods_text'], second=test_text, msg='上传模板商品失败')


if __name__ == '__main__':
    unittest.main()
    # test_case = unittest.TestLoader().loadTestsFromTestCase(TestRun)
    # BeautifulReport.BeautifulReport(
    #   test_case).report(filename='login_report', description='登录自动化', report_dir='../Report')
