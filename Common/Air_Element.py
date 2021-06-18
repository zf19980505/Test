class ApiBaserPage:
    # 初始化基础类
    def __init__(self, air_poco, air_api):
        self.air_poco = air_poco
        self.air_api = air_api

    # poco定位元素
    def poco_element(self, air_locator):
        return self.air_poco(**air_locator)

    def poco_click(self, air_locator=None, air_new=None):
        if air_new is None:
            self.poco_element(air_locator).click()
        else:
            air_new.click()

    def poco_send_keys(self, value, air_locator=None, air_new=None):
        if air_new is None:
            self.poco_element(air_locator).send_keys(value)
        else:
            air_new.send_keys(value)

    def poco_text(self, air_locator=None, air_new=None):
        if air_new is None:
            return self.poco_element(air_locator).get_text()
        else:
            return air_new.get_text()

    def poco_exists(self, air_locator):
        return self.poco_element(air_locator).exists()

    def poco_swipe(self, air_locator, value):
        air_size = self.poco_element(air_locator).get_size()
        width = air_size[0]
        height = air_size[1]
        x1 = float(value[0])
        y1 = float(value[1])
        x2 = float(value[2])
        y2 = float(value[3])
        self.air_poco.swipe([width * x1, height * y1], [width * x2, height * y2])

    # 通过图片比对，然后点击
    def api_touch(self, api_locator):
        self.air_api.touch(self.air_api.Template(r'' + api_locator))

    def api_exists(self, api_locator):
        return self.air_api.exists(self.air_api.Template(r'' + api_locator))

    def api_keyevent(self, api_data):
        self.air_api.keyevent(api_data)

    # 返回键
    def api_return(self):
        self.api_keyevent('KEYCODE_BACK')