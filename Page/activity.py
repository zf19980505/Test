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
    def new_groud(self, activitys_el, newgroud_el, group_data, groud_el):
        # 转换数据类型
        groud_activity = self.str_by_tuple(activitys_el['groud_activity'])
        groud_list = self.str_by_tuple(activitys_el['groud_list'])
        goods_numberone = self.str_by_tuple(groud_el['goods_numberone'])
        goods_number_tr = self.str_by_tuple(groud_el['goods_number_tr'])
        new_groud = self.str_by_tuple(newgroud_el['new'])
        time_el = self.str_by_tuple(newgroud_el['time'])
        start_time = self.str_by_tuple(newgroud_el['start_time'])
        end_date = self.str_by_tuple(newgroud_el['end_date'])
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
        goods_numone = self.locator_element(locator=goods_numberone, locators=goods_number_tr)
        number = 0
        for group_lis in goods_numone:
            number = number + 1
            self.groups = group_lis.find_elements_by_xpath(groud_el['goods_number_td'])
        self.group_spu_number = number
        # 新建拼团活动按钮
        self.click(locator=new_groud, locators=None)
        # 打开新建时间
        self.click(locator=time_el, locators=None)
        # 获取明天日期
        end_dates = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        sleep(1)
        # 模拟ctrl + a全选
        self.keyboard_Ctrl(locator=start_time, locators=None, value=group_data['groud_ctrl'])
        self.send_key(locator=start_time, locators=None, value=group_data['start_end_times'])
        # 结束时间
        self.keyboard_Ctrl(locator=end_date, locators=None, value=group_data['groud_ctrl'])
        self.send_key(locator=end_date, locators=None, value=end_dates)
        self.keyboard_Ctrl(locator=end_time, locators=None, value=group_data['groud_ctrl'])
        self.send_key(locator=end_time, locators=None, value=group_data['start_end_times'])
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
        group_spu_lis = self.locator_element(locator=group_spuone, locators=group_sputwo)
        for group_spus in group_spu_lis:
            group_spu = group_spus.find_elements_by_xpath(newgroud_el['group_sputhree'])
            i = 0
            while True:
                # 死循环为了拿到大于供货价小于零售价的拼团价格
                i = i + 1
                # 根据供货价和零售价生成拼团价格，拼团价格取两个价格中间
                groud_price = random.uniform(float(group_spu[4].text), float(group_spu[5].text))
                # 拼团价格包留两位小数
                groud_prices = round(groud_price, 2)
                print('单个sku供货价：', float(group_spu[4].text))
                print('单个sku零售价：', float(group_spu[5].text))
                print('单个sku的拼团价格：', groud_prices)
                if float(group_spu[4].text) < groud_prices < float(group_spu[5].text):
                    group_spu[6].find_element_by_class_name(group_data['groud_price']).send_keys(str(groud_prices))
                    break
            # 拿到该拼团商品的spu
            self.new_textone = group_spu[0].text
        self.click(locator=new_submit, locators=None)
        goods_numone = self.locator_element(locator=goods_numberone, locators=goods_number_tr)
        for group_lis in goods_numone:
            self.groups = group_lis.find_elements_by_xpath(groud_el['goods_number_td'])
            if self.groups[3].text == self.new_textone:
                self.new_texttwo = self.groups[3].text

    # 删除拼团
    def delete_group(self, groud_el):
        # 转换数据类型
        goods_numberone = self.str_by_tuple(groud_el['goods_numberone'])
        goods_number_tr = self.str_by_tuple(groud_el['goods_number_tr'])
        grouds_delete = self.str_by_tuple(groud_el['grouds_delete'])
        goods_numone = self.locator_element(locator=goods_numberone, locators=goods_number_tr)
        for group_lis in goods_numone:
            groups = group_lis.find_elements_by_xpath(groud_el['goods_number_td'])
            if self.new_textone == groups[3].text:
                self.group_text = groups[3].text
                # 点击删除按钮
                groups[8].click()
                # 点击删除的二次确认
                self.click(locator=grouds_delete, locators=None)
                sleep(2)
        # 重新获取当前拼团列表
        again_group_lis = self.locator_element(locator=goods_numberone, locators=goods_number_tr)
        for again_groups in again_group_lis:
            again_groups = again_groups.find_elements_by_xpath(groud_el['goods_number_td'])
            if again_groups[3].text == self.group_text:
                self.delete_text = 'false'
        self.delete_text = 'true'
