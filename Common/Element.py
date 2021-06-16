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
    def locator_element(self, locator=None, locators=None, new_el=None):
        if new_el is not None:
            if locators is not None and locator is not None:
                locatorkey, locator_value = locator
                locatorkeys, locator_values = locators
                return new_el.find_element(locatorkey, locator_value).find_elements(locatorkeys, locator_values)

            elif locators is not None and locator is None:
                locatorkeys, locator_values = locators
                return new_el.find_elements(locatorkeys, locator_values)

            elif locators is None and locator is not None:
                locatorkeys, locator_values = locator
                return new_el.find_element(locatorkeys, locator_values)

            else:
                return new_el

        elif locators is None:
            locatorkey, locator_value = locator
            return self.driver.find_element(locatorkey, locator_value)

        else:
            locatorkey, locator_value = locator
            locatorkeys, locator_values = locators
            return self.driver.find_element(locatorkey, locator_value).find_elements(locatorkeys, locator_values)

    def locator_elements(self, locator):
        locatorkey, locator_value = locator
        return self.driver.find_elements(locatorkey, locator_value)

    def send_key(self, value, locator=None, locators=None, new_el=None):
        if new_el is not None:
            new_el.send_keys(value)
        else:
            self.locator_element(locator, locators).send_keys(value)

    def click(self, locator=None, locators=None, new_el=None):
        if new_el is not None:
            new_el.click()
        else:
            self.locator_element(locator, locators).click()

    def locator_text(self, locator=None, locators=None, new_el=None):
        if new_el is not None:
            return new_el.text
        else:
            return self.locator_element(locator, locators).text

    # 关闭浏览器
    def quit(self):
        self.driver.quit()

    # 模拟键盘Ctrl + 任意键
    def keyboard_Ctrl(self, value, locator=None, locators=None, new_el=None):
        keyboard_value = self.keyboard.CONTROL + value
        if new_el is not None:
            self.send_key(value=keyboard_value, new_el=new_el)
        else:
            self.send_key(value=keyboard_value, locator=locator, locators=locators)

    # 刷新当前页面
    def refresh(self):
        self.driver.refresh()

    # 新建标签页
    def new_tab(self):
        new_windows = 'window.open()'
        self.driver.execute_script(new_windows)
        admin = self.driver.window_handles[0]
        back = self.driver.window_handles[1]
        return admin, back

    # 切换标签页
    def cut_tab(self, tab):
        self.driver.switch_to.window(tab)