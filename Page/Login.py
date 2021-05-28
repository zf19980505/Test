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

    def close(self):
        self.quit()
