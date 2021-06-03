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
        self.click(locator=new_coupons['new'], locators=None)
        self.send_key(locator=new_coupons['coupons_name'], locators=None, value=element_data['coupons_name'])