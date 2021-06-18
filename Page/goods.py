from Common.Element import *
from Common.req_Element import *
from time import sleep
import random
import json


class Goods(BaserPage):
    # 旺店通拉取商品
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
        goods_lis = list(set(self.spu_lis).difference(set(goods_spu_lis)))
        if goods_lis:
            print('未拉取到的spu：', goods_lis)
            return False
        else:
            return True

    # 总部上架商品
    def up_down_goods(self, elemter, goods_data, page=None, up_down=None, delete=None):
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
            if up_down is None:
                # 上架
                self.click(new_el=public_button[goods_data['up_button_path']])
            elif delete is None:
                # 下架
                self.click(new_el=public_button[goods_data['down_button_path']])
            else:
                # 删除
                self.click(new_el=public_button[goods_data['delete_button_path']])
            # 把标签页切换到分销
            self.cut_tab(goods_data['back'])
            sleep(2)
            return admin_up_goods
        else:
            spu_lis = []
            self.refresh()
            # 拿到所有商品
            sleep(2)
            goods = self.locator_element(locator=elemter['back_tbody'], locators=elemter['public_tr'])
            for public_tr in goods:
                public_td = self.locator_element(new_el=public_tr, locators=elemter['public_td'])
                spu = self.locator_text(new_el=public_td[goods_data['back_spu_path']])
                spu_lis.append(spu)
            if up_down is None:
                # 上架
                up_goods = list(set(page).difference(set(spu_lis)))
            else:
                # 下架/删除
                up_goods = list(set(page).intersection(set(spu_lis)))
            self.cut_tab(goods_data['admin'])
            if up_goods:
                return False
            else:
                return True

    # 编辑商品
    def edit_goods(self, elemter, goods_data):
        tr_number = self.locator_element(locator=elemter['admin_tbody'], locators=elemter['public_tr'])
        for tr in tr_number:
            td_number = self.locator_element(new_el=tr, locators=elemter['public_td'])
            if self.locator_text(new_el=td_number[goods_data['goods_spu_path']]) == goods_data['goods_spu']:
                # 拿到tr里边的所有button
                public_button = self.locator_element(new_el=td_number[-1], locators=elemter['public_button'])
                # 最后一个就是编辑，所以选择最后一个点击打开编辑页面
                self.click(new_el=public_button[-1])
                self.hovering(action_el=elemter['goods_master_map'])
                self.click(locator=elemter['master_map_delete'])
                sleep(2)
                # 拿到所有上传的input框
                pubilc_up_input = self.locator_elements(locator=elemter['pubilc_up_input'])
                self.send_key(new_el=pubilc_up_input[goods_data['master_map_path']], value=goods_data['master_map'])
                sleep(2)
                # 拿到编辑页面里面的所有button
                pubilc_content = self.locator_elements(locator=elemter['pubilc_content'])
                edit_submit = self.locator_element(new_el=pubilc_content[-1], locators=elemter['public_button'])
                self.click(new_el=edit_submit[goods_data['edit_submit']])
                sleep(2)
                break


class Req_goods(BaserRequest):
    def look_goods(self, url, params):
        res = self.get(url=url, params=params['look_spu_data'])
        res_text = json.loads(res.text)
        if res_text['code'] != 200:
            return None
        plist = res_text['PList']
        for goods_number in plist:
            for goods_key, goods_val in dict.items(goods_number):
                if goods_val == params['spu_name']:
                    return goods_number[params['master_map']]
