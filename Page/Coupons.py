from Common.Air_Element import *
from Common.Element import *
from Common.req_Element import *
from airtest.core.api import *
from time import sleep
import random
import re
import json


# todo seleuimUI
class Coupons_el(BaserPage):
    # 新建优惠卷
    def new_coupons(self, element_data, new_coupons, coupons_lis):
        self.click(locator=new_coupons['new'], locators=None)
        sleep(2)
        coupons_inputs = self.locator_elements(new_coupons['coupons_inputs'])
        # 输入优惠卷的名称
        self.send_key(value=element_data['coupons_name'], new_el=coupons_inputs[0])
        # 满多少减多少的这个钱随机生成0-1的两位数小数
        full_money = random.uniform(0.2, 1.0)
        full_money = round(full_money, 2)
        subtract_money = random.uniform(0.1, full_money)
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
            # 先设置好商品分类的下标位置，方便后边用到
            goods_category_number = 6
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
            # 先设置好商品分类的下标位置，方便后边用到
            goods_category_number = 7
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
            self.click(new_el=coupons_inputs[goods_category_number])
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
        sleep(2)
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
                if self.locator_text(new_el=coupons_td[2]) == self.grant_text:
                    self.coupons_key = self.locator_text(new_el=coupons_td[2])
                    return self.coupons_key
            self.coupons_key = '优惠卷发放失败'
        except Exception as e:
            print(e)
            self.coupons_key = '优惠卷发放失败，进入不到下一个页面'

    # 新建开屏红包
    def new_coupon_envelope(self, envelope_el, element_data, envelope_lis):
        # 点击新建开屏红包
        self.click(locator=envelope_el['new'])
        # 拿到当前页面上的所有input框
        public_input = self.locator_elements(locator=envelope_el['public_input'])
        # 输入开屏红包的名称
        self.send_key(new_el=public_input[element_data['envelope_name_path']], value=element_data['envelope_name'])
        # 打开优惠券的key的下拉框
        self.click(new_el=public_input[element_data['envelope_key_path']])
        # 拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=envelope_el['dropdown_box'])
        # 当前打开的下拉框在页面上总是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=envelope_el['public_li'])
        # 最新的优惠卷处于下拉框的第一位，所以默认取第一位
        self.click(new_el=dropdown_box_li[0])
        # 设置新建红包图片
        self.send_key(locator=envelope_el['envelope_photo'], value=element_data['envelope_photo'])
        # 点击投放时间
        self.click(new_el=public_input[element_data['time_path']])
        # 因为input数量变化了,重新拿到当前页面上的所有input框
        public_input = self.locator_elements(locator=envelope_el['public_input'])
        # 开始时间
        self.keyboard_Ctrl(new_el=public_input[element_data['start_time_path']], value=element_data['ctrl_a'])
        self.send_key(new_el=public_input[element_data['start_time_path']], value=element_data['start_end_times'])
        # 结束日期
        self.keyboard_Ctrl(new_el=public_input[element_data['end_date_path']], value=element_data['ctrl_a'])
        self.send_key(new_el=public_input[element_data['end_date_path']], value=element_data['end_dates'])
        # 结束时间
        self.keyboard_Ctrl(new_el=public_input[element_data['end_time_path']], value=element_data['ctrl_a'])
        self.send_key(new_el=public_input[element_data['end_time_path']], value=element_data['start_end_times'])
        # 提交时间
        self.click(locator=envelope_el['time_submit'], locators=None)
        # 点击跳转类型拿到跳转类型的下拉框
        self.click(new_el=public_input[element_data['skip_type_path']])
        # 因为跳转类型再次拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=envelope_el['dropdown_box'])
        # 当前打开的下拉框在页面上总是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=envelope_el['public_li'])
        # 只有一个跳转区域，就是商品区域
        self.click(new_el=dropdown_box_li[0])
        # 因为input数量变化了,重新拿到当前页面上的所有input框
        public_input = self.locator_elements(locator=envelope_el['public_input'])
        # 打开spu编码的下拉框
        self.click(new_el=public_input[element_data['spu_path']])
        # 因为spu编码需要再次拿到所有的下拉框
        dropdown_box = self.locator_elements(locator=envelope_el['dropdown_box'])
        # 当前打开的下拉框在页面上总是最后一个，所以取最后一个来取得当前下拉框里的内容
        dropdown_box_li = self.locator_element(new_el=dropdown_box[-1], locators=envelope_el['public_li'])
        # 默认选择第一个，但是这是不对的得封装成一个方法
        self.click(new_el=dropdown_box_li[0])
        # 选择启用该红包
        self.click(locator=envelope_el['start_using'])
        # 提交保存
        self.click(locator=envelope_el['submit'])
        sleep(5)
        # 断言阶段
        try:
            # 拿到优惠卷页面的所有优惠卷，然后断言是否新建成功
            envelope_body = self.locator_element(locator=envelope_lis['envelope_body'], locators=envelope_lis['public_tr'])
            for envelope_tr in envelope_body:
                envelope_td = self.locator_element(new_el=envelope_tr, locators=envelope_lis['public_td'])
                if self.locator_text(new_el=envelope_td[1]) == element_data['envelope_name']:
                    self.envelope_text = self.locator_text(new_el=envelope_td[1])
                    return self.envelope_text
            self.envelope_text = '新建开屏红包失败'
        except Exception as e:
            print(e)
            self.envelope_text = '新建开屏红包失败，进入不到下一个页面'


# todo 接口
class Req_coupons(BaserRequest):
    # 查看小程序领券中心里的所有优惠券
    def xcx_look_coupons(self, url, params, headers, public_data):
        res = self.get(url=url, params=params, headers=headers)
        res_text = res.text
        # 正则提取返回信息
        re_data = re.findall(public_data['public_data'] + '(.*?)},', res_text)
        for i in re_data:
            dict_data = json.loads(i)
            if dict_data['coupon_node'] == public_data['coupons_key']:
                self.get_coupons_text = dict_data['coupon_node']
                return self.get_coupons_text
        self.get_coupons_text = '找不到该优惠卷'

    # 用户领取优惠卷
    def xcx_get_coupons(self, url, data, headers):
        res = self.post(url=url, data=data, headers=headers)
        get_coupons_res = eval(res.text)
        if get_coupons_res['code'] == 200:
            self.get_coupons_text = 'True'
        else:
            self.get_coupons_text = 'False'


# todo AirtestUI
class Air_coupons(ApiBaserPage):
    def look_grant_coupons(self, air_el, air_swipe):
        self.poco_click(air_locator=air_el['xcx_my'])
        for i in range(10):
            if self.poco_exists(air_locator=air_el['xcx_grant_coupons']):
                self.poco_click(air_locator=air_el['xcx_grant_coupons'])
                break
            else:
                sleep(1)
                self.poco_swipe(air_locator=air_el['xcx_page'], value=air_swipe['xcx_swipe'])

        for i in range(10):
            if self.poco_exists(air_locator=air_el['coupons_name']):
                self.air_grant_coupons_text = 'True'
                self.poco_click(air_locator=air_el['xcx_return'])
                self.poco_click(air_locator=air_el['xcx_home'])
                return self.air_grant_coupons_text
            else:
                sleep(1)
                self.poco_swipe(air_locator=air_el['xcx_page'], value=air_swipe['xcx_swipe'])
        self.poco_click(air_locator=air_el['xcx_return'])
        self.poco_click(air_locator=air_el['xcx_home'])
        self.air_grant_coupons_text = 'False'
