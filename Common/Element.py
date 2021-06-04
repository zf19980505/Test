class BaserPage:
    # 初始化基础类
    def __init__(self, driver, keyboard):
        self.driver = driver
        self.keyboard = keyboard
        self.driver.implicitly_wait(60)

    # 启动浏览器，访问指定页面
    def open(self, url):
        self.driver.get(url)
        # self.driver.maximize_window()

    # 定位元素
    def locator_element(self, locator, locators):
        if locators is None:
            locatorkey, locator_value = locator
            return self.driver.find_element(locatorkey, locator_value)
        else:
            locatorkey, locator_value = locator
            locatorkeys, locator_values = locators
            return self.driver.find_element(locatorkey, locator_value).find_elements(locatorkeys, locator_values)

    def send_key(self, locator, locators, value):
        self.locator_element(locator, locators).send_keys(value)

    def click(self, locator, locators):
        self.locator_element(locator, locators).click()

    def locator_text(self, locator, locators):
        return self.locator_element(locator, locators).text

    # 关闭浏览器
    def quit(self):
        self.driver.quit()

    # 模拟键盘Ctrl + 任意键
    def keyboard_Ctrl(self, locator, locators, value):
        keyboard_value = self.keyboard.CONTROL + value
        self.send_key(locator, locators, keyboard_value)
