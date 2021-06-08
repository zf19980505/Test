from Common.Air_Element import *
from Common.Element import *
from Common.req_Element import *
from airtest.core.api import *
from time import sleep
import random


class Coupons_el(BaserPage):
    # 新建优惠卷
    def New_Coupons(self, element_data, new_coupons, coupons_lis):
        self.click(locator=new_coupons['new'], locators=None)
        sleep(2)
        coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
        # 输入优惠卷的名称
        self.send_key(value=element_data['coupons_name'], new_el=coupons_inputs[0])
        # 满多少减多少的这个钱随机生成0-1的两位数小数
        full_money = random.uniform(0.0, 1.0)
        full_money = round(full_money, 2)
        subtract_money = random.uniform(0.0, full_money)
        subtract_money = round(subtract_money, 2)
        # 输入满多少
        self.send_key(value=str(full_money), new_el=coupons_inputs[1])
        # 输入减多少
        self.send_key(value=str(subtract_money), new_el=coupons_inputs[2])
        # 优惠卷的有效期类型
        self.click(new_el=coupons_inputs[3])
        # 拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=new_coupons['dropdown_box'])
        # 当前下拉框都是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=new_coupons['public_li'])
        date_type_number = random.randint(0, len(dropdown_box_li) - 1)
        sleep(2)
        if self.locator_text(new_el=dropdown_box_li[date_type_number]) == element_data['coupons_date_type']:
            # 固定日期的逻辑
            self.click(new_el=dropdown_box_li[date_type_number])
            sleep(2)
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 先设置好优惠券限制的下标位置，方便后边用到
            value_date = 5
            # 打开新建时间
            self.click(new_el=coupons_inputs[4])
            sleep(2)
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 开始时间
            self.keyboard_Ctrl(new_el=coupons_inputs[7], value=element_data['ctrl_a'])
            self.send_key(new_el=coupons_inputs[7], value=element_data['start_end_times'])
            # 结束日期
            self.keyboard_Ctrl(new_el=coupons_inputs[8], value=element_data['ctrl_a'])
            self.send_key(new_el=coupons_inputs[8], value=element_data['end_dates'])
            # 结束时间
            self.keyboard_Ctrl(new_el=coupons_inputs[9], value=element_data['ctrl_a'])
            self.send_key(new_el=coupons_inputs[9], value=element_data['start_end_times'])
            # 提交时间
            self.click(locator=new_coupons['time_submit'], locators=None)
        else:
            # 动态日期的逻辑
            self.click(new_el=dropdown_box_li[date_type_number])
            sleep(2)
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 先设置好优惠券限制的下标位置，方便后边用到
            value_date = 6
            # 领卷后N天后生效
            self.send_key(new_el=coupons_inputs[4], value=element_data['dynamic_time'])
            # 领卷后有效持续天数
            self.send_key(new_el=coupons_inputs[5], value=element_data['continue_time'])
        # 根据之前设置好的下标位置，打开优惠卷限制的下拉框
        self.click(new_el=coupons_inputs[value_date])
        # 再次拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=new_coupons['dropdown_box'])
        # 当前下拉框都是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=new_coupons['public_li'])
        date_type_number = random.randint(0, len(dropdown_box_li) - 1)
        sleep(2)
        if self.locator_text(new_el=dropdown_box_li[date_type_number]) == element_data['continue_restrict']:
            # 如果是优惠卷限制里的全部通用，那就直接保存
            self.click(new_el=dropdown_box_li[date_type_number])
        else:
            # 如果不是全部通用，则重新获取当前所有的input框的长度
            self.click(new_el=dropdown_box_li[date_type_number])
            sleep(2)
            coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
            # 根据最后一次获取到的input框的长度，取倒数第二个，点击打开指定商品分类的下拉框
            self.click(new_el=coupons_inputs[-1])
            # 再次拿到所有的下拉框
            dropdown_box = self.locator_elements(locator=new_coupons['dropdown_box'])
            # 当前下拉框都是最后一个，所以取最后一个来取得当前下拉框里的内容
            dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=new_coupons['public_li'])
            date_type_number = random.randint(0, len(dropdown_box_li) - 1)
            # 根据生成的随机数去随机选取到商品的分类
            self.click(new_el=dropdown_box_li[date_type_number])
        # 最后的保存
        self.click(locator=new_coupons['coupons_submit'])
        sleep(5)
        try:
            # 拿到优惠卷页面的所有优惠卷，然后断言是否新建成功
            coupons_body = self.locator_element(locator=coupons_lis['coupons_body'], locators=coupons_lis['public_tr'])
            for coupons_tr in coupons_body:
                coupons_td = self.locator_element(new_el=coupons_tr, locators=coupons_lis['public_td'])
                if self.locator_text(new_el=coupons_td[1]) == element_data['coupons_name']:
                    self.coupons_name = self.locator_text(new_el=coupons_td[1])
                    return self.coupons_name
            self.coupons_name = '新建失败'
        except Exception as e:
            print(e)
            self.coupons_name = '优惠卷新建失败，进入不到下一个页面'

    # 发放优惠卷
    def grant_coupons(self, coupons_el, element_data, coupons_lis):
        self.click(locator=coupons_el['grant_button'])
        # 先拿到发放页面的所有input输入框
        grant_input = self.locator_elements(locator=coupons_el['grant_input'])
        self.click(new_el=grant_input[0])
        # 拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=coupons_el['dropdown_box'])
        # 当前下拉框都是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=coupons_el['public_li'])
        # 取到要选择的优惠卷的key存起来方便后面断言
        self.grant_text = self.locator_text(new_el=dropdown_box_li[0])
        # 最新的优惠卷处于下拉框的第一位，所以默认取第一位
        self.click(new_el=dropdown_box_li[0])
        # 每日限量
        self.send_key(new_el=grant_input[1], value=element_data['daily_limited'])
        # 每人总限量
        self.send_key(new_el=grant_input[2], value=element_data['everyone_limit'])
        # 打开发放时间
        self.click(new_el=grant_input[3])
        # 重新获取一次页面上的input框
        grant_input = self.locator_elements(locator=coupons_el['grant_input'])
        # 开始时间
        self.keyboard_Ctrl(new_el=grant_input[6], value=element_data['ctrl_a'])
        self.send_key(new_el=grant_input[6], value=element_data['start_end_times'])
        # 结束日期
        self.keyboard_Ctrl(new_el=grant_input[7], value=element_data['ctrl_a'])
        self.send_key(new_el=grant_input[7], value=element_data['end_dates'])
        # 结束时间
        self.keyboard_Ctrl(new_el=grant_input[8], value=element_data['ctrl_a'])
        self.send_key(new_el=grant_input[8], value=element_data['start_end_times'])
        # 提交时间
        self.click(locator=coupons_el['time_submit'])
        # 打开是否发放
        self.click(new_el=grant_input[4])
        # 再次拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=coupons_el['dropdown_box'])
        # 当前下拉框都是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=coupons_el['public_li'])
        # 发放处于下拉框第一位，所以默认取第一个
        self.click(new_el=dropdown_box_li[0])
        self.click(locator=coupons_el['grant_submit'])
        sleep(5)
        # 断言阶段
        try:
            # 拿到优惠卷页面的所有优惠卷，然后断言是否新建成功
            coupons_body = self.locator_element(locator=coupons_lis['coupons_body'], locators=coupons_lis['public_tr'])
            for coupons_tr in coupons_body:
                coupons_td = self.locator_element(new_el=coupons_tr, locators=coupons_lis['public_td'])
                self.coupons_key = self.locator_text(new_el=coupons_td[2])
        except Exception as e:
            print(e)
            self.coupons_key = '优惠卷发放失败，进入不到下一个页面'
