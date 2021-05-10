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
        # 进入商品列表
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[2]/div/span').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[2]/ul/li').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button[3]/span').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[6]/div/div[2]/form/div/div/div/div[1]/input').click()
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/ul/li[1]/span').click()
        # text = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[4]/div/ul').find_elements_by_xpath('li')
        # self.driver.find_element_by_xpath(
        #     '//*[@id="app"]/div/div[2]/div[2]/div/div/div[4]/div/span/div/input').send_keys(Keys.BACK_SPACE)
        # self.driver.find_element_by_xpath(
        #     '//*[@id="app"]/div/div[2]/div[2]/div/div/div[4]/div/span/div/input').send_keys(len(text))
        # self.driver.find_element_by_xpath(
        #     '//*[@id="app"]/div/div[2]/div[2]/div/div/div[4]/div/span/div/input').send_keys(Keys.ENTER)
        # sleep(1)
        # test = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[3]/div/div[3]/table/tbody').find_elements_by_class_name('el-table__row')
        # print(len(test))
        # b = 0
        # for jishu in test:
        #     b = b+1
        # print(b)
        print('-------结束前三秒------------')
        sleep(3)
        self.driver.quit()


if __name__ == '__main__':
    test_run = Test()
    test_run.test_one()
