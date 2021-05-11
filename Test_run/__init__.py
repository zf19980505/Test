from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Test:
    def test_one(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://wscadmin.xcxback.cn/admin/')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[1]/div/div/input').send_keys('ceshi4')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[2]/div/div[1]/input').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[3]/div/button').click()
        # 拼团开始
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/div/span').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/ul/li[1]').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button/span').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/form/div[1]/div/div/input[1]').click()
        sleep(2)
        print('---------选择时间开始前--------')
        # self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/table/tbody/tr[4]/td[3]').click()
        # self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/table/tbody/tr[4]/td[4]/div/span').click()
        test = self.driver.find_element_by_class_name('el-date-table__row')
        print('--------', test)
        self.driver.find_element_by_class_name('available').click()
        print('-------选择时间结束前三秒------------')
        sleep(3)
        self.driver.quit()


if __name__ == '__main__':
    test_run = Test()
    test_run.test_one()
