from Common.Element import *
from time import sleep
import random


class Test(BaserPage):
    def menu_module(self, menu_path, element_data):
        menu_modules = self.locator_element(locator=menu_path['menu_management'], locators=menu_path['menu_modules'])
        for modus_lis in menu_modules:
            if modus_lis.text == element_data['moules_lis_name']:
                modus_lis.click()
                modus = modus_lis.find_element_by_class_name(element_data['modus_lis']).find_elements_by_xpath(
                    element_data['modus'])
                for module_name in modus:
                    if module_name.text == element_data['modus_name']:
                        module_name.click()
                        break
                break

    def add_group(self, goods_area, element_data):
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
                self.add_goods_text = area_td[3].text
                print('该拼团商品已存在')
                break
            self.click(locator=goods_area['add_goods_button'], locators=None)
            # 通过循环tr拿到单个区域列表的内容
            add_goods_tbody = self.locator_element(locator=goods_area['add_goods_tbody'], locators=goods_area['public_tr'])
            for add_tr in add_goods_tbody:
                add_td = add_tr.find_elements(td_key, td_val)
                if add_td[4].text == self.new_textone:
                    add_td[0].find_element_by_xpath('div/label/span/span').click()
                    self.click(locator=goods_area['add_goods_submit'], locators=None)
                    # 重新获取商品区域里边的所有商品，以作断言看看刚刚添加进去的商品是否添加成功
                    area_tr = self.locator_element(locator=goods_area['area_tbody'], locators=goods_area['public_tr'])
                    # 通过循环tr拿到单行的列表的内容
                    for tr in area_tr:
                        area_td = tr.find_elements(td_key, td_val)
                        if area_td[3].text == self.new_textone:
                            self.add_goods_text = area_td[3].text
                            print('该拼团商品添加成功')
                            break
                    break