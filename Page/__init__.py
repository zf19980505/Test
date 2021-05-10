from selenium import webdriver
from time import sleep


class Test:
    def test_one(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://sbt-hk.zgserver.cn')
        self.driver.find_element_by_xpath('/html/body/section/div[1]/div/div/a').click()
        # 登录黄渔国
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[1]/div/div/input').send_keys('ceshi2')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]/div/div/input').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[3]/div/button/span').click()
        sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    test_run = Test()
    test_run.test_one()
