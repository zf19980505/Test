from Common.Air_Element import *
from Common.Element import *
from Common.req_Element import *
from airtest.core.api import *
from time import sleep
import random
import datetime


class Coupons_el(BaserPage):
    # 新建拼团
    def New_Coupons(self, element_data, new_coupons):
        public_li_key, public_li_value = element_data['public_li']
        self.click(locator=new_coupons['new'], locators=None)
        self.send_key(locator=new_coupons['coupons_name'], locators=None, value=element_data['coupons_name'])
        # 满多少减多少的这个钱随机生成0-1的两位数小数
        full_money = random.uniform(0.0, 1.0)
        full_money = round(full_money, 2)
        subtract_money = random.uniform(0.0, full_money)
        subtract_money = round(subtract_money, 2)
        self.send_key(locator=new_coupons['full_money'], locators=None, value=full_money)
        self.send_key(locator=new_coupons['subtract_money'], locators=None, value=subtract_money)
        self.click(locator=new_coupons['coupons_datetype_input'], locators=None)

        coupons_date_type = self.locator_element(locator=new_coupons['coupons_date_type'],
                                                 locators=element_data['public_ul'])
        date_type_number = random.randint(0, len(coupons_date_type))
        if coupons_date_type[date_type_number].find_elements(public_li_key, public_li_value).text == element_data['coupons_date_type']:
            # 固定日期的逻辑
            coupons_date_type[date_type_number].find_elements(public_li_key, public_li_value).click()
            # 打开新建时间
            self.click(locator=new_coupons['time'], locators=None)
            # 开始时间
            self.keyboard_Ctrl(locator=new_coupons['start_time'], locators=None, value=element_data['ctrl_a'])
            self.send_key(locator=new_coupons['start_time'], locators=None, value=element_data['start_end_times'])
            # 结束时间
            self.keyboard_Ctrl(locator=new_coupons['end_date'], locators=None, value=element_data['ctrl_a'])
            self.send_key(locator=new_coupons['end_date'], locators=None, value=element_data['end_dates'])
            self.keyboard_Ctrl(locator=new_coupons['end_time'], locators=None, value=element_data['ctrl_a'])
            self.send_key(locator=new_coupons['end_time'], locators=None, value=element_data['start_end_times'])
            # 提交时间
            self.click(locator=new_coupons['time_submit'], locators=None)
        else:
            # 动态日期的逻辑
            self.send_key(locator=new_coupons['dynamic_time'], locators=None, value=element_data['dynamic_time'])
            self.send_key(locator=new_coupons['continue_time'], locators=None, value=element_data['continue_time'])

        self.click(locator=new_coupons['continue_restrict'], locators=None)
        continue_restrict_lis = self.locator_element(locator=new_coupons['continue_restrict_lis'],
                                                     locators=element_data['public_ul'])
        continue_restrict_number = random.randint(0, len(continue_restrict_lis))
        # 如果他选中指定分类
        if continue_restrict_lis[continue_restrict_number].find_elements(public_li_key, public_li_value).text == element_data['continue_restrict']:
            self.click(locator=new_coupons['coupons_submit'], locators=None)
        else:
            # 指定分类/指定spu编码input框里的内容
            self.click(locator=new_coupons['appoint'], locators=None)
            appoint_lis = self.locator_element(locator=new_coupons['appoint_lis'], locators=element_data['public_ul'])
            appoint_number = random.randint(0, len(appoint_lis) - 1)
            appoint_lis[appoint_number].click()
            self.click(locator=new_coupons['continue_restrict_submit'], locators=None)