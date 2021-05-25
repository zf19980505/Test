from Common.Element import *
from time import sleep
from selenium.webdriver.common.keys import Keys


class Goods(BaserPage):
    # def login(self, username, password, url, elemter):
    #     # 转换数据类型
    #     user_name = self.str_by_tuple(elemter['username'])
    #     user_password = self.str_by_tuple(elemter['password'])
    #     user_submit = self.str_by_tuple(elemter['submit'])
    #     user_text = self.str_by_tuple(elemter['text'])
    #     # 业务实现
    #     self.open(url=url)
    #     self.send_key(locator=user_name, locators=None, value=username)
    #     self.send_key(locator=user_password, locators=None, value=password)
    #     self.click(locator=user_submit, locators=None)
    #     self.login_text = self.locator_text(locator=user_text, locators=None)

    def upload_goods(self, elemter, goods_spu_ex):
        # 转换数据类型
        goods_administrations = self.str_by_tuple(elemter['goods_administrations'])
        goods_list = self.str_by_tuple(elemter['goods_list'])
        goods_template = self.str_by_tuple(elemter['goods_template'])
        pitch_on_one = self.str_by_tuple(elemter['pitch_on_one'])
        pitch_on_two = self.str_by_tuple(elemter['pitch_on_two'])
        submit_two = self.str_by_tuple(elemter['submit_two'])
        page_turning = self.str_by_tuple(elemter['page_turning'])
        goods_spu_text = self.str_by_tuple(elemter['goods_spu_text'])
        # 业务实现
        # 商品管理
        self.click(locator=goods_administrations, locators=None)
        # 商品列表
        self.click(locator=goods_list, locators=None)
        # # 点击上传模板
        # self.click(locator=goods_template, locators=None)
        # # 点击选择运费模板
        # self.click(locator=pitch_on_one, locators=None)
        # # 选择第一个运费模板
        # self.click(locator=pitch_on_two, locators=None)
        # # 上传商品
        # self.send_key(locator=submit_two, locators=None, value=goods_spu_ex)
        # sleep(3)
        # # 进入第二页
        # self.click(locator=page_turning, locators=None)
        sleep(1)
        # 断言校验结果
        self.goods_spu_text = self.locator_text(locator=goods_spu_text, locators=None)
        print('--------两秒后结束测试--------')
        sleep(2)
        self.quit()