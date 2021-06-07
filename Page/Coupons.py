from Common.Air_Element import *
from Common.Element import *
from Common.req_Element import *
from airtest.core.api import *
from time import sleep
import random
import datetime


class Coupons_el(BaserPage):
    def Coupons_tbody(self, coupons_lis):
        coupons_body = self.locator_element(locator=coupons_lis['coupons_body'], locators=coupons_lis['public_tr'])
        for coupons_tr in coupons_body:
            coupons_td = self.locator_element(new_el=coupons_tr, locators=coupons_lis['public_td'])
            self.coupons_name = self.locator_text(new_el=coupons_td[1])

    # 新建优惠卷
    def New_Coupons(self, element_data, new_coupons):
        self.click(locator=new_coupons['new'], locators=None)
        coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
        self.send_key(value=element_data['coupons_name'], new_el=coupons_inputs[0])
        # 满多少减多少的这个钱随机生成0-1的两位数小数
        full_money = random.uniform(0.0, 1.0)
        full_money = round(full_money, 2)
        subtract_money = random.uniform(0.0, full_money)
        subtract_money = round(subtract_money, 2)
        self.send_key(value=str(full_money), new_el=coupons_inputs[1])
        self.send_key(value=str(subtract_money), new_el=coupons_inputs[2])
        self.click(new_el=coupons_inputs[3])
        coupons_date_type = self.locator_element(locator=new_coupons['coupons_date_type'],
                                                 locators=new_coupons['public_li'])
        date_type_number = random.randint(0, len(coupons_date_type) - 1)
        if self.locator_text(new_el=coupons_date_type[date_type_number]) == element_data['coupons_date_type']:
            self.click(new_el=coupons_date_type[date_type_number])
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 固定日期的逻辑
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
            self.click(new_el=coupons_date_type[date_type_number])
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 动态日期的逻辑
            self.click(new_el=coupons_inputs[4])
            self.send_key(locator=new_coupons['dynamic_time'], locators=None, value=element_data['dynamic_time'])
            self.send_key(locator=new_coupons['continue_time'], locators=None, value=element_data['continue_time'])

        self.click(new_el=coupons_inputs[len(coupons_inputs) - 1])
        sleep(2)
        # 优惠券限制
        continue_restrict_ul = self.locator_elements(locator=new_coupons['continue_restrict'])
        continue_restrict = self.locator_element(locators=new_coupons['public_li'], new_el=continue_restrict_ul[-1])
        continue_restrict_number = random.randint(0, len(continue_restrict) - 1)
        if self.locator_text(new_el=continue_restrict[continue_restrict_number]) == element_data['continue_restrict']:
            self.click(new_el=continue_restrict[continue_restrict_number])
        else:
            self.click(new_el=continue_restrict[continue_restrict_number])
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            sleep(2)
            self.click(new_el=coupons_inputs[len(coupons_inputs) - 1])
            sleep(2)
            appoint_ul = self.locator_elements(locator=new_coupons['continue_restrict'])
            appoint = self.locator_element(locators=new_coupons['public_li'], new_el=appoint_ul[-1])
            appoint_number = random.randint(0, len(appoint) - 1)
            self.click(new_el=appoint[appoint_number])
        # print('结束前5秒')
        # sleep(5)
        self.click(locator=new_coupons['coupons_submit'])