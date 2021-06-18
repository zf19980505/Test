from Common.Element import *
from Common.Air_Element import *
from time import sleep


class LayoutPage(BaserPage):
    # 新建首页商品商品版块
    def new_home_layout(self, layout_el, layout_data, public_el, page=None):
        if page is None:
            # todo 总部
            # 拿到页面所有按钮，点击新建按钮
            sleep(2)
            public_button = self.locator_elements(locator=public_el['public_button'])
            self.click(new_el=public_button[layout_data['new_home_layout']])
            # 拿到新建页面的所有input框
            public_input = self.locator_elements(locator=public_el['public_input'])
            # 输入新建板块名称
            self.send_key(new_el=public_input[layout_data['home_layout_path']], value=layout_data['home_layout_name'])
            self.click(locator=public_el['home_start_using'])
            self.send_key(new_el=public_input[layout_data['home_sort']], value=layout_data['home_sort'])
            # 获取到新建页面的所有按钮，点击保存
            new_layout_button = self.locator_elements(locator=public_el['public_button'])
            self.click(new_el=new_layout_button[layout_data['home_layout_submit']])
            sleep(2)
            # 获取页面body以作断言
            tr_number = self.locator_element(locator=layout_el['adminhome_layout_tbody'],
                                             locators=public_el['public_tr'])
            for tr in tr_number:
                td_number = self.locator_element(new_el=tr, locators=public_el['public_td'])
                if self.locator_text(new_el=td_number[layout_data['home_name_path']]) == layout_data['home_layout_name']:
                    # 切换到分销页面
                    self.cut_tab(layout_data['back'])
                    return True
            return False
        else:
            # todo 分销
            # 获取页面body以作断言
            tr_number = self.locator_element(locator=layout_el['backhome_layout_tbody'],
                                             locators=public_el['public_tr'])
            for tr in tr_number:
                td_number = self.locator_element(new_el=tr, locators=public_el['public_td'])
                if self.locator_text(new_el=td_number[layout_data['home_name_path']]) == layout_data['home_layout_name']:
                    self.cut_tab(layout_data['admin'])
                    return True
            self.cut_tab(layout_data['admin'])
            return False

    # 商品区域一排一新建
    def new_goods_area(self, area_el, area_data, public_el, page=None):
        if page is None:
            # todo 总部
            # 拿到页面所有按钮，点击新建按钮
            sleep(2)
            public_button = self.locator_elements(locator=public_el['public_button'])
            self.click(new_el=public_button[area_data['new_button']])
            public_input = self.locator_elements(locator=public_el['public_input'])
            self.send_key(new_el=public_input[area_data['new_one_area_path']], value=area_data['one_area_name'])
            # 拿到新建的确认按钮
            new_area_submit = self.locator_element(locator=area_el['new_area_button'],
                                                   locators=area_el['new_area_submit'])
            self.click(new_el=new_area_submit[-1])
            sleep(2)
            # 获取页面body以作断言
            tr_number = self.locator_element(locator=area_el['admin_goodsarea_tbody'],
                                             locators=public_el['public_tr'])
            for tr in tr_number:
                td_number = self.locator_element(new_el=tr, locators=public_el['public_td'])
                if self.locator_text(new_el=td_number[area_data['one_area_path']]) == area_data['one_area_name']:
                    one_area_coding = self.locator_text(new_el=td_number[area_data['one_area_coding']])
                    # 切换到分销页面
                    self.cut_tab(area_data['back'])
                    return one_area_coding
            return False
        else:
            # todo 分销
            # 获取页面body以作断言
            tr_number = self.locator_element(locator=area_el['back_goodsarea_tbody'],
                                             locators=public_el['public_tr'])
            for tr in tr_number:
                td_number = self.locator_element(new_el=tr, locators=public_el['public_td'])
                if self.locator_text(new_el=td_number[area_data['one_area_coding']]) == page:
                    self.cut_tab(area_data['admin'])
                    return True
            self.cut_tab(area_data['admin'])
            return False

    # 把商品区域加入首页商品板块
    def area_join_layout(self, layout_el, layout_data, public_el, page=None):
        if page is None:
            self.locator_element()


class LayoutAir(ApiBaserPage):
    def xcx_look_homelayout(self, air_el, air_data):
        self.poco_click(air_locator=air_el['wx_more'])
        wx_refresh = self.poco_element(air_locator=air_el['wx_refresh'])
        self.poco_click(air_new=wx_refresh[air_data['wx_refresh_path']])
        for i in range(10):
            if self.poco_exists(air_locator=air_el['new_home_name']):
                return True
            else:
                sleep(2)
        return False
