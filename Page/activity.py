from Common.Element import *
from time import sleep
from selenium.webdriver.common.keys import Keys


class Activity(BaserPage):
    # 用户登录
    def login(self, username, password, url, elemter):
        # 转换数据类型
        user_name = self.str_by_tuple(elemter['username'])
        user_password = self.str_by_tuple(elemter['password'])
        user_submit = self.str_by_tuple(elemter['submit'])
        user_text = self.str_by_tuple(elemter['text'])
        # 业务实现
        self.open(url=url)
        self.send_key(locator=user_name, locators=None, value=username)
        self.send_key(locator=user_password, locators=None, value=password)
        self.click(locator=user_submit, locators=None)
        self.login_text = self.locator_text(locator=user_text, locators=None)

    # 新建拼团
    def new_groud(self, activitys_el, groud_el):
        # 转换数据类型
        groud_activity = self.str_by_tuple(activitys_el['groud_activity'])
        groud_list = self.str_by_tuple(activitys_el['groud_list'])
        new_groud = self.str_by_tuple(groud_el['new'])
        time = self.str_by_tuple(groud_el['time'])
        start_time = self.str_by_tuple(groud_el['start_time'])
        end_time = self.str_by_tuple(groud_el['end_time'])
        # 活动管理
        self.click(locator=groud_activity, locators=None)
        # 拼团活动列表
        self.click(locator=groud_list, locators=None)
        # 新建拼团活动按钮
        self.click(locator=new_groud, locators=None)
        sleep(2)
        print('--------1')
        # 打开新建时间
        self.click(locator=time, locators=None)
        print('--------2')
        self.click(locator=start_time, locators=None)
        print('--------3')
        self.click(locator=end_time, locators=None)
        print('--------4')
        sleep(2)
        self.quit()
