class ApiBaserPage:
    # 初始化基础类
    def __init__(self, air_driver):
        self.air_driver = air_driver

    # poco定位元素
    def air_element(self, air_locator):
        return self.air_driver(**air_locator)

    def air_click(self, air_locator):
        self.air_element(**air_locator).click()
