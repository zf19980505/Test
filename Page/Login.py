from Common.Element import *
from Common.Air_Element import *
from Common.req_Element import *
from time import sleep


class Login_server(BaserPage):
    # 用户登录
    def logins(self, username, password, url, elemter):
        # 业务实现
        self.open(url=url)
        self.send_key(locator=elemter['username'], locators=None, value=username)
        self.send_key(locator=elemter['password'], locators=None, value=password)
        self.click(locator=elemter['submit'], locators=None)
        sleep(5)
        self.login_text = self.locator_text(locator=elemter['text'], locators=None)

    # 拿到首页菜单
    def menu_module(self, menu_path, element_data=None, again_menu=None):
        if again_menu is None:
            menu_modules = self.locator_element(locator=menu_path['menu_management'],
                                                locators=menu_path['menu_modules'])
            for modus_lis_name in menu_modules:
                if modus_lis_name.text == element_data['moules_lis_name']:
                    sleep(1)
                    modus_lis_name.click()
                    modus = self.locator_element(locator=menu_path['modus_lis'], locators=menu_path['modus'])
                    for module_name in modus:
                        if module_name.text == element_data['modus_name']:
                            sleep(1)
                            module_name.click()
                            break
                    break
        else:
            sleep(2)
            modus = self.locator_element(locator=menu_path['modus_lis'], locators=menu_path['modus'])
            for module_name in modus:
                if module_name.text == again_menu['modus_name']:
                    sleep(1)
                    module_name.click()
                    break

    # 关闭浏览器
    def close(self):
        self.quit()


class Air_Loging(ApiBaserPage):
    def xcx_login(self, air_el, air_swipe, air_data):
        self.poco_click(air_locator=air_el['app'])
        self.poco_swipe(air_locator=air_el['weixin_name'], value=air_swipe['weixin_swipe'])
        sleep(2)
        xcx = self.poco_element(air_locator=air_el['xcx_lis'])
        sleep(2)
        for i in xcx:
            i.get_text()
            if i.get_text() == air_data['xcx_name']:
                i.click()
                break

        self.poco_click(air_locator=air_el['xcx_class'])
        self.poco_click(air_locator=air_el['xcx_login_button'])
        self.poco_click(air_locator=air_el['xcx_login_submit'])
        # 循环10秒查看是否登录
        for i in range(10):
            sleep(1)
            if self.api_exists(api_locator=air_data['xcx_notlogin']):
                self.xcx_login_text = 'False'
            else:
                self.xcx_login_text = 'True'
                self.poco_click(air_locator=air_el['xcx_home_page'])
                return self.xcx_login_text


class Req_login(BaserRequest):
    def req_login(self, url, data):
        res = self.post(url=url, data=data)
        for key, val in dict.items(eval(res)):
            if key == 'token':
                self.token = {'Authorization': val}
            elif key == 'username':
                self.username = val
        self.username = 'False'
