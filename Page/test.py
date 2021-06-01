from Common.Air_Element import *
from Common.req_Element import *
from time import sleep
from airtest.core.api import *


class Airtest_Server(ApiBaserPage):
    def test_wx(self, air_el, air_data):
        self.poco_click(air_locator=air_el['app'])
        self.poco_swipe(air_locator=air_el['weixin_name'], value=air_data['weixin_swipe'])
        sleep(2)
        xcx = self.poco_element(air_locator=air_el['xcx'])
        sleep(2)
        for i in xcx:
            i.get_text()
            if i.get_text() == 'AR试鞋':
                i.click()
                break


class Req_login(BaserRequest):
    def req_login(self, url, data):
        res = self.post(url=url, data=data)
        for key, val in dict.items(eval(res.text)):
            if key == 'token':
                self.token = {'Authorization': val}
            elif key == 'username':
                self.username = val
        self.username = 'False'

    def gruop_goods_lis(self, url, params, public_data):
        res = self.get(url=url, params=params)
        for key, val in dict.items(eval(res.text)):
            if key == public_data['groupList']:
                for two_val in val:
                    print(two_val)
                    if two_val['spu_code'] == 'SPU2021536910001':
                        self.group_id = two_val['id']

