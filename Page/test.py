from Common.Air_Element import *
from Common.req_Element import *
from time import sleep
from airtest.core.api import *


class Airtest_Server(ApiBaserPage):
    def test_wx(self, air_el, air_swipe, air_data):
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

    def test_airpay(self, air_data):
        self.api_touch(api_locator=air_data['xcx_group_buttom'])
        self.api_touch(api_locator=air_data['xcx_group_pay_buttom'])
        self.api_touch(api_locator=air_data['xcx_group_pay_submit'])
        if self.api_exists(api_locator=air_data['xcx_wx_pay']):
            keyboard_Lis = list(air_data['xcx_keyboard'].split(','))
            for keyboard_data in keyboard_Lis:
                self.api_keyevent(keyboard_data)
        for i in range(10):
            if self.api_exists(api_locator=air_data['xcx_group_pay_complete']):
                self.api_touch(air_data['xcx_group_pay_complete'])
                sleep(5)
                break
            else:
                sleep(1)


class Req_login(BaserRequest):
    def req_login(self, url, data):
        res = self.post(url=url, data=data)
        for key, val in dict.items(eval(res.text)):
            if key == 'token':
                self.token = {'Authorization': val}
            elif key == 'username':
                self.username = val
        self.username = 'False'

    def test_group_lis(self, url, params, public_data):
        res = self.get(url=url, params=params)
        for key, val in dict.items(eval(res.text)):
            if key == public_data['groupList']:
                for two_val in val:
                    if two_val['spu_code'] == public_data['spucode']:
                        self.group_id = two_val['id']
                        return self.group_id

    def test_dele_group(self, url, params):
        res = self.delete(url=url, params=params)
        delete_res = eval(res.text)
        if delete_res['code'] == 500:
            self.delete_text = 'False'
        else:
            self.delete_text = 'True'
