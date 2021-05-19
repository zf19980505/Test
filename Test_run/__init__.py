from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random


class Test:
    def test_one(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://testadmin.3dshowarea.com/admin/')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[1]/div/div/input').send_keys('ceshi4')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[2]/div/div[1]/input').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[3]/div/button').click()
        # 拼团开始
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/div/span').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/ul/li[1]').click()
        # self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button/span').click()
        sleep(2)
        print('---------选择时间开始前--------')
        test = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/table/tbody').find_elements_by_xpath('tr')
        group_spu_number = len(test)
        print(group_spu_number)
        a = test[group_spu_number - 1].find_elements_by_xpath('td')
        print('不是0：', a[3].text)
        print('-------选择时间结束前三秒------------')
        # sleep(3)
        self.driver.quit()


if __name__ == '__main__':
    test_run = Test()
    test_run.test_one()
