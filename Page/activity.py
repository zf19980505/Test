from Common.Element import *
from Common.Air_Element import *
from time import sleep
from selenium.webdriver.common.keys import Keys
import random


class Activity(BaserPage):
    # # 用户登录
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

    # 新建拼团
    def new_groud(self, activitys_el, newgroud_el, group_data, groud_el):
        # 转换数据类型
        groud_activity = self.str_by_tuple(activitys_el['groud_activity'])
        groud_list = self.str_by_tuple(activitys_el['groud_list'])
        goods_numberone = self.str_by_tuple(groud_el['goods_numberone'])
        goods_numbertwo = self.str_by_tuple(groud_el['goods_numbertwo'])
        new_groud = self.str_by_tuple(newgroud_el['new'])
        time = self.str_by_tuple(newgroud_el['time'])
        start_time = self.str_by_tuple(newgroud_el['start_time'])
        end_time = self.str_by_tuple(newgroud_el['end_time'])
        time_submit = self.str_by_tuple(newgroud_el['time_submit'])
        group_order_time = self.str_by_tuple(newgroud_el['group_order_time'])
        group_order_number = self.str_by_tuple(newgroud_el['group_order_number'])
        group_spulist = self.str_by_tuple(newgroud_el['group_spulist'])
        spu_listone = self.str_by_tuple(newgroud_el['spu_listone'])
        spu_listtwo = self.str_by_tuple(newgroud_el['spu_listtwo'])
        group_spuone = self.str_by_tuple(newgroud_el['group_spuone'])
        group_sputwo = self.str_by_tuple(newgroud_el['group_sputwo'])
        new_submit = self.str_by_tuple(newgroud_el['new_submit'])
        # 活动管理
        self.click(locator=groud_activity, locators=None)
        # 拼团活动列表
        self.click(locator=groud_list, locators=None)
        goods_num = self.locator_element(locator=goods_numberone, locators=goods_numbertwo)
        group_spu_number = len(goods_num)
        # 新建拼团活动按钮
        self.click(locator=new_groud, locators=None)
        # 打开新建时间
        self.click(locator=time, locators=None)
        sleep(1)
        self.click(locator=start_time, locators=None)
        self.click(locator=end_time, locators=None)
        self.click(locator=time_submit, locators=None)
        # =========================================
        self.send_key(locator=group_order_time, locators=None, value=group_data['date_order_time'])
        self.send_key(locator=group_order_number, locators=None, value=group_data['date_order_number'])
        # =========选择设置拼团商品============
        self.click(locator=group_spulist, locators=None)
        group_spulis = self.locator_element(locator=spu_listone, locators=spu_listtwo)
        # 生成随机数,并且随机选择商品
        if len(group_spulis) >= 8:
            random_number = random.randint(0, 7)
        else:
            random_number = random.randint(0, len(group_spulis) - 1)
        group_spulis[random_number].click()
        group_spu = self.locator_element(locator=group_spuone, locators=group_sputwo)
        groud_price = random.uniform(float(group_spu[4].text), float(group_spu[5].text))
        groud_prices = round(groud_price, 2)
        group_spu[6].find_element_by_class_name(group_data['groud_price']).send_keys(str(groud_prices))
        self.new_textone = group_spu[0].text
        self.click(locator=new_submit, locators=None)
        goods_numone = self.locator_element(locator=goods_numberone, locators=goods_numbertwo)
        group_goods = goods_numone[group_spu_number].find_elements_by_xpath('td')
        sleep(5)
        self.new_texttwo = group_goods[3].text
        # self.quit()

