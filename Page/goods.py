from Common.Element import *
from time import sleep
import random


class Goods(BaserPage):
    def upload_goods(self, elemter, goods_data):
        self.spu_lis = []
        # 点击上传模板
        self.click(locator=elemter['goods_template'], locators=None)
        # 获取到页面上所有的input框
        public_input = self.locator_elements(locator=elemter['public_input'])
        # 运费模板是最后一位所以默认取最后一个
        self.click(new_el=public_input[-1])
        # 取到页面上所有的ul
        public_ul = self.locator_elements(locator=elemter['public_ul'])
        # 取到运费模板里所有运费
        public_li = self.locator_element(new_el=public_ul[-1], locators=elemter['public_li'])
        # 第一个是包邮，默认取第一个，也可以取随机
        self.click(new_el=public_li[0])
        # 上传商品
        self.send_key(locator=elemter['upload_spu'], locators=None, value=goods_data['goods_spu_ex'])
        # 拿到上传所有商品，因旺店通逻辑一个商品一秒，所以，取到当前所有xls里的长度-1就是要拉取的商品数量
        goods_spu_lis = goods_data['goods_spu']
        sleep(len(goods_spu_lis) + 2)
        # 刷新页面
        self.refresh()
        # 拿到当前页面的表单元素
        tr_number = self.locator_element(locator=elemter['admin_tbody'], locators=elemter['public_tr'])
        for public_tr in tr_number:
            td_number = self.locator_element(new_el=public_tr, locators=elemter['public_td'])
            spu = self.locator_text(new_el=td_number[goods_data['admin_spu_path']])
            self.spu_lis.append(spu)
        goods_lis = set(self.spu_lis).intersection(set(goods_spu_lis))
        if len(goods_lis) == len(goods_spu_lis):
            return True
        else:
            return False

    def up_goods(self, elemter, goods_data, page=None):
        if page is None:
            admin_up_goods = []
            # 拿到所有商品
            goods = self.locator_element(locator=elemter['admin_tbody'], locators=elemter['public_tr'])
            # 根据商品的数量来生成随机数
            goods_random = random.randint(1, len(goods))
            # 拿到所有商品勾选框
            check_goods = self.locator_elements(locator=elemter['check_goods'])
            a = 0
            # 根据生成的随机数来决定勾选几个商品
            for i in range(goods_random):
                public_td = self.locator_element(new_el=goods[0 + a], locators=elemter['public_td'])
                # 通过循环把要勾选的商品的spu储存起来
                admin_up_goods.append(self.locator_text(new_el=public_td[goods_data['admin_spu_path']]))
                # 通过循环勾选商品
                self.click(new_el=check_goods[1 + a])
                a += 1
            # 拿到页面上所有的button，根据下标点击上架按钮
            public_button = self.locator_elements(locator=elemter['public_button'])
            self.click(new_el=public_button[goods_data['up_button_path']])
            # 把标签页切换到分销
            self.cut_tab(goods_data['back'])
            sleep(2)
            return admin_up_goods
        else:
            spu_lis = []
            # 拿到所有商品
            sleep(2)
            goods = self.locator_element(locator=elemter['back_tbody'], locators=elemter['public_tr'])
            for public_tr in goods:
                public_td = self.locator_element(new_el=public_tr, locators=elemter['public_td'])
                spu = self.locator_text(new_el=public_td[goods_data['back_spu_path']])
                spu_lis.append(spu)
            up_goods = list(set(page).difference(set(spu_lis)))
            if up_goods:
                print('未显示的spu', up_goods)
                return False
            else:
                return True