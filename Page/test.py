from Common.Air_Element import *
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

        # self.poco_click(air_locator=air_el['xcx_class'])
        # self.poco_click(air_el['xcx_class_module'])
        # page = self.poco_element(air_locator=air_el['xcx_page'])
        # for a in page:
        #     print(a.get_text())
        #     if a.get_text() == '拼团商品':
        #         a.click()
        # # while True:
        # #     print('开始寻找')
        # #     if self.air_exists(air_el['xcx_modules_name']):
        # #         self.air_click(air_el['xcx_modules_name'])
        # #         break
        # #     else:
        # #         print('没有该元素')
        # # 死循环只为了找到该拼团商品
        # i = 0
        # while True:
        #     i = i + 1
        #     if self.api_exists(api_locator=air_el['xcx_group_good']):
        #         self.api_touch(air_el['xcx_group_good'])
        #         break
        #     else:
        #         print('找不到拼团商品的话，往上滑动页面寻找该商品')
        #         self.poco_swipe(air_el['xcx_page'], value=air_data['xcx_swipe'])
            # if exists((Template(r'' + air_el['xcx_group_good'], record_pos=(-0.011, 0.431), resolution=(1080, 2160)))):
            #     touch((Template(r'' + air_el['xcx_group_good'], record_pos=(-0.011, 0.431), resolution=(1080, 2160))))
            #     break
            # else:
            #     print('找不到拼团商品的话，往上滑动页面寻找该商品')
            #     self.air_swipe(air_el['xcx_page'], value=air_data['xcx_swipe'])
