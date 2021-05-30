from Common.Element import *
from time import sleep
import random
import datetime


class Test(BaserPage):
    def deleeter_group(self, goods_area, element_data):
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
                deleter_buttons = self.locator_element(locator=goods_area['delete_goods'], locators=goods_area['delete_goods_submit'])
                sleep(3)
                deleter_buttons[1].click()
                # 重新获取商品区域里边的所有商品，以作断言看看刚刚添加进去的商品是否添加成功
                area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
                # 通过循环tr拿到单行的列表的内容
                for tr in area_tr:
                    area_td = tr.find_elements(td_key, td_val)
                    if area_td[3].text == self.new_textone:
                        print('删除拼团商品添加失败')
                        self.add_goods_text = 'False'
                        return self.add_goods_text
        self.add_goods_text = 'True'