from Common.Element import *
from time import sleep


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
        tr_number = self.locator_element(locator=elemter['public_tbody'], locators=elemter['public_tr'])
        for public_tr in tr_number:
            td_number = self.locator_element(new_el=public_tr, locators=elemter['public_td'])
            spu = self.locator_text(new_el=td_number[goods_data['spu_path']])
            self.spu_lis.append(spu)
        goods_lis = set(self.spu_lis).intersection(set(goods_spu_lis))
        if len(goods_lis) == len(goods_spu_lis):
            return True
        else:
            return False
