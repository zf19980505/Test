class ApiBaserPage:
    # 初始化基础类
    def __init__(self, air_driver):
        self.air_driver = air_driver

    # poco定位元素
    def air_element(self, air_locator):
        return self.air_driver(**air_locator)

    def air_click(self, air_locator):
        self.air_element(air_locator).click()

    def air_send_keys(self, air_locator, value):
        self.air_element(air_locator).send_keys(value)

    def air_text(self, air_locator):
        return self.air_element(air_locator).get_text()

    def air_exists(self, air_locator):
        return self.air_element(air_locator).exists()

    def air_swipe(self, air_locator, value):
        air_size = self.air_element(air_locator).get_size()
        width = air_size[0]
        height = air_size[1]
        x1 = float(value[0])
        y1 = float(value[1])
        x2 = float(value[2])
        y2 = float(value[3])
        self.air_driver.swipe([width * x1, height * y1], [width * x2, height * y2])
