from Common.Element import *
from time import sleep


class Login_server(BaserPage):
    # 用户登录
    def logins(self, username, password, url, elemter):
        # 转换数据类型
        user_name = self.str_by_tuple(elemter['username'])
        user_password = self.str_by_tuple(elemter['password'])
        user_submit = self.str_by_tuple(elemter['submit'])
        user_text = self.str_by_tuple(elemter['text'])
        # 业务实现
        self.open(url=url)
        self.send_key(locator=user_name, locators=None, value=username)
        self.send_key(locator=user_password, locators=None, value=password)
        self.click(locator=user_submit, locators=None)
        sleep(5)
        self.login_text = self.locator_text(locator=user_text, locators=None)

    def close(self):
        self.quit()
