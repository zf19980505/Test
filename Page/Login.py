from Common.Element import *
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
    def menu_module(self, menu_path, element_data):
        menu_modules = self.locator_element(locator=menu_path['menu_management'],
                                            locators=menu_path['menu_modules'])
        for modus_lis in menu_modules:
            if modus_lis.text == element_data['moules_lis_name']:
                modus_lis.click()
                modus = modus_lis.find_element_by_class_name(element_data['modus_lis']).find_elements_by_xpath(
                    element_data['modus'])
                for module_name in modus:
                    if module_name.text == element_data['modus_name']:
                        module_name.click()
                        break
                break

    # 关闭浏览器
    def close(self):
        self.quit()
