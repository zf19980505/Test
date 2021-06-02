from Common.Air_Element import *
from Common.Element import *
from Common.req_Element import *
from airtest.core.api import *
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
    def new_groud(self, element_data, group, new_group):
        # # 获取拼团活动里的所有拼团商品
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
        # todo 通过循环拿到固定的单个商品以便作为拼团商品
        for group_spu in group_spulis:
            if group_spu.text == element_data['group_name']:
                group_spu.click()
        # todo 通过生成随机数点击随机商品
        # # 生成随机数,并且随机选择商品
        # if len(group_spulis) >= 8:
        #     random_number = random.randint(0, 7)
        # else:
        #     random_number = random.randint(0, len(group_spulis) - 1)
        # # 选择拼团商品
        # group_spulis[random_number].click()
        group_goods_lis = self.locator_element(locator=new_group['group_spuone'], locators=new_group['group_sput_tr'])
        for group_spus in group_goods_lis:
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
        print('删除商品')
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

    # 把拼团商品添加进入布局
    def add_area_group(self, goods_area, element_data):
        # 拿到当前所有商品布局内容
        td_key, td_val = goods_area['public_td']
        area_button_key, area_button_val = goods_area['area_button']
        # 通过循环tr拿到单行的列表的内容
        area_lis_tr = self.locator_element(locator=goods_area['area_lis_tbody'], locators=goods_area['public_tr'])
        for lis_tr in area_lis_tr:
            area_td = lis_tr.find_elements(td_key, td_val)
            if area_td[1].text == element_data['area_name']:
                area_buttons = area_td[3].find_elements(area_button_key, area_button_val)
                area_buttons[2].click()
                break
        area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
        # 通过循环tr拿到区域列表单行的列表的内容
        for tr in area_tr:
            area_td = tr.find_elements(td_key, td_val)
            if area_td[3].text == self.new_textone:
                print('该拼团商品已存在')
                self.add_goods_text = 'True'
                return self.add_goods_text
        self.click(locator=goods_area['add_goods_button'], locators=None)
        # 通过循环tr拿到添加商品列表的内容
        add_goods_tbody = self.locator_element(locator=goods_area['add_goods_tbody'], locators=goods_area['public_tr'])
        for add_tr in add_goods_tbody:
            add_td = add_tr.find_elements(td_key, td_val)
            if add_td[4].text != self.new_textone:
                self.add_goods_text = 'False'
            else:
                add_td[0].find_element_by_xpath('div/label/span/span').click()
                self.click(locator=goods_area['add_goods_submit'], locators=None)
                sleep(3)
                # 重新获取商品区域里边的所有商品，以作断言看看刚刚添加进去的商品是否添加成功
                area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
                # 通过循环tr拿到单行的列表的内容
                for tr in area_tr:
                    area_td = tr.find_elements(td_key, td_val)
                    if area_td[3].text == self.new_textone:
                        print('该拼团商品添加成功')
                        self.add_goods_text = 'True'
                        return self.add_goods_text

    # 把拼团商品从布局里删除
    def deleter_area_group(self, goods_area, element_data):
        # 拿到当前所有商品布局内容
        td_key, td_val = goods_area['public_td']
        area_button_key, area_button_val = goods_area['area_button']
        # 通过循环tr拿到单行的列表的内容
        area_lis_tr = self.locator_element(locator=goods_area['area_lis_tbody'], locators=goods_area['public_tr'])
        for lis_tr in area_lis_tr:
            area_td = lis_tr.find_elements(td_key, td_val)
            if area_td[1].text == element_data['area_name']:
                area_buttons = area_td[3].find_elements(area_button_key, area_button_val)
                area_buttons[2].click()
                break
        area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
        # 通过循环tr拿到区域列表单行的列表的内容
        for tr in area_tr:
            area_td = tr.find_elements(td_key, td_val)
            if area_td[3].text == self.new_textone:
                print('该拼团商品已存在')
                buttons = area_td[6].find_elements_by_xpath('div/button')
                buttons[1].click()
                sleep(3)
                deleter_buttons = self.locator_element(locator=goods_area['delete_goods'],
                                                       locators=goods_area['delete_goods_submit'])
                sleep(3)
                deleter_buttons[1].click()
                sleep(3)
                # 重新获取商品区域里边的所有商品，以作断言看看刚刚添加进去的商品是否添加成功
                area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
                # 通过循环tr拿到单行的列表的内容
                for tr in area_tr:
                    area_td = tr.find_elements(td_key, td_val)
                    if area_td[3].text == self.new_textone:
                        print('删除拼团商品添加失败')
                        self.delete_goods_text = 'False'
                        return self.delete_goods_text
        self.delete_goods_text = 'True'


class Air_Activity(ApiBaserPage, metaclass=Singleton):
    # 打开小程序查看该商品是否是拼团商品
    def xcx_group(self, air_el, air_swipe, air_data):
        self.poco_click(air_locator=air_el['app'])
        self.poco_swipe(air_locator=air_el['weixin_name'], value=air_swipe['weixin_swipe'])
        sleep(2)
        xcx = self.poco_element(air_locator=air_el['xcx'])
        sleep(2)
        for i in xcx:
            i.get_text()
            if i.get_text() == air_data['xcx_name']:
                i.click()
                break
        while True:
            if self.api_exists(api_locator=air_data['xcx_group_good']):
                self.api_touch(api_locator=air_data['xcx_group_good'])
                # 循环20秒等待找到元素
                for i in range(10):
                    if self.api_exists(api_locator=air_data['xcx_group_buttom']):
                        self.xcx_group_text = 'True'
                        return self.xcx_group_text
                    else:
                        sleep(2)
                self.xcx_group_text = 'Fales'
                break
            else:
                self.poco_swipe(air_locator=air_el['xcx_page'], value=air_swipe['xcx_swipe'])


class Req_Activity(BaserRequest, metaclass=Singleton):
    # 拿到当前拼团列表里的所有拼团
    def gruop_goods_lis(self, url, params, public_data):
        res = self.get(url=url, params=params)
        for key, val in dict.items(eval(res.text)):
            if key == public_data['groupList']:
                for two_val in val:
                    if two_val['spu_code'] == public_data['spucode']:
                        self.group_id = two_val['id']

    def delete_group_good(self, url, params):
        res = self.delete(url=url, params=params)
        delete_res = eval(res.text)
        if delete_res['code'] == 500:
            self.delete_text = 'False'
        else:
            self.delete_text = 'True'