from Common.Element import *
from time import sleep
import random
import datetime


# 加载单例模式
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Activity(BaserPage, metaclass=Singleton):
    # 新建拼团
    def new_groud(self, menu_path, element_data, group, new_group):
        menu_modules = self.locator_element(locator=menu_path['menu_management'], locators=menu_path['menu_modules'])
        for modus_lis in menu_modules:
            if modus_lis.text == element_data['moules_lis_name']:
                modus_lis.click()
                modus = modus_lis.find_element_by_class_name(element_data['modus_lis']).find_elements_by_xpath(element_data['modus'])
                for module_name in modus:
                    if module_name.text == element_data['modus_name']:
                        module_name.click()
                        break
                break
        # 获取拼团活动里的所有拼团商品
        # group_goods = self.locator_element(locator=group['group_lis'], locators=group['group_goods_tr'])
        # if len(group_goods) != 0:
        #     self.gruop_goods_len = len(group_goods)
        # 新建拼团
        self.click(locator=new_group['new'], locators=None)
        # 打开新建时间
        self.click(locator=new_group['time'], locators=None)
        # 获取明天日期
        end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # 开始时间
        self.keyboard_Ctrl(locator=new_group['start_time'], locators=None, value=element_data['ctrl_a'])
        self.send_key(locator=new_group['start_time'], locators=None, value=element_data['start_end_times'])
        # 结束时间
        self.keyboard_Ctrl(locator=new_group['end_date'], locators=None, value=element_data['ctrl_a'])
        self.send_key(locator=new_group['end_date'], locators=None, value=end_dates)
        self.keyboard_Ctrl(locator=new_group['end_time'], locators=None, value=element_data['ctrl_a'])
        self.send_key(locator=new_group['end_time'], locators=None, value=element_data['start_end_times'])
        # 提交时间
        self.click(locator=new_group['time_submit'], locators=None)
        # =========选择设置拼团有效期和人数============
        self.send_key(locator=new_group['group_order_time'], locators=None, value=element_data['date_order_time'])
        self.send_key(locator=new_group['group_order_number'], locators=None, value=element_data['date_order_number'])
        # =========选择设置拼团商品============
        self.click(locator=new_group['group_spulist'], locators=None)
        group_spulis = self.locator_element(locator=new_group['spu_listone'], locators=new_group['spu_listtwo'])
        # 生成随机数,并且随机选择商品
        if len(group_spulis) >= 8:
            random_number = random.randint(0, 7)
        else:
            random_number = random.randint(0, len(group_spulis) - 1)
        group_spulis[random_number].click()
        group_spu_lis = self.locator_element(locator=new_group['group_spuone'], locators=new_group['group_sput_tr'])
        for group_spus in group_spu_lis:
            locatorkeys, locator_values = new_group['group_spu_td']
            group_spu = group_spus.find_elements(locatorkeys, locator_values)
            i = 0
            while True:
                # 死循环为了拿到大于供货价小于零售价的拼团价格
                i = i + 1
                # 根据供货价和零售价生成拼团价格，拼团价格取两个价格中间
                groud_price = random.uniform(float(group_spu[4].text), float(group_spu[5].text))
                # 拼团价格包留两位小数
                groud_prices = round(groud_price, 2)
                # print('单个sku供货价：', float(group_spu[4].text))
                # print('单个sku零售价：', float(group_spu[5].text))
                # print('单个sku的拼团价格：', groud_prices)
                if float(group_spu[4].text) < groud_prices < float(group_spu[5].text):
                    price_keys, price_values = new_group['groud_price']
                    group_spu[6].find_element(price_keys, price_values).send_keys(str(groud_prices))
                    break
            # 拿到该拼团商品的spu
            self.new_textone = group_spu[0].text
        self.click(locator=new_group['new_submit'], locators=None)
        goods_numone = self.locator_element(locator=group['group_lis'], locators=group['group_goods_tr'])
        for group_lis in goods_numone:
            new_goods_key, new_goods_values = group['group_goods_td']
            self.groups = group_lis.find_elements(new_goods_key, new_goods_values)
            if self.groups[3].text == self.new_textone:
                self.new_texttwo = self.groups[3].text

    # 删除拼团
    def delete_group(self, groud_el):
        # 获取到拼团列表所有拼团商品
        goods_numone = self.locator_element(locator=groud_el['group_lis'], locators=groud_el['group_goods_tr'])
        # 把元素td拆出来，方便定位方法直接使用
        self.delete_group_key, self.delete_group_value = groud_el['group_goods_td']
        for group_lis in goods_numone:
            groups = group_lis.find_elements(self.delete_group_key, self.delete_group_value)
            if self.new_textone == groups[3].text:
                self.group_text = groups[3].text
                # 点击删除按钮
                sleep(3)
                groups[8].find_element_by_xpath('div/button').click()
                sleep(2)
                # 点击删除的二次确认
                self.click(locator=groud_el['group_delete'], locators=None)
                sleep(3)
                break
        # 重新获取当前拼团列表里的所有拼团商品以做断言校验
        again_group_lis = self.locator_element(locator=groud_el['group_lis'], locators=groud_el['group_goods_tr'])
        for again_groups in again_group_lis:
            again_groups = again_groups.find_elements(self.delete_group_key, self.delete_group_value)
            if again_groups[3].text == self.group_text:
                self.delete_text = 'false'
        self.delete_text = 'true'
