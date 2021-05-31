from Common.Air_Element import *
from time import sleep
from airtest.core.api import *


class Airtest_Server(ApiBaserPage):
    def test_wx(self, air_el, air_data):
        self.air_click(air_locator=air_el['app'])
        self.air_swipe(air_locator=air_el['weixin_name'], value=air_data['weixin_swipe'])
        sleep(2)
        xcx = self.air_element(air_locator=air_el['xcx'])
        sleep(2)
        for i in xcx:
            i.get_text()
            if i.get_text() == 'AR试鞋':
                i.click()
                break
        self.air_click(air_locator=air_el['xcx_class'])
        self.air_click(air_el['xcx_class_module'])
        sleep(2)
        self.air_click(air_el['xcx_modules_name'])
        # 死循环只为了找到该拼团商品
        i = 0
        while True:
            i = i + 1
            if exists((Template(r'' + air_el['xcx_group_good'], record_pos=(-0.011, 0.431), resolution=(1080, 2160)))):
                touch((Template(r'' + air_el['xcx_group_good'], record_pos=(-0.011, 0.431), resolution=(1080, 2160))))
                break
            else:
                print('找不到拼团商品的话，往上滑动页面寻找该商品')
                self.air_swipe(air_el['xcx_page'], value=air_data['xcx_swipe'])
