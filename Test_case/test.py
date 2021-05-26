from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://testadmin.3dshowarea.com/admin/')
# 登录
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[1]/div/div/input').send_keys('ceshi4')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[2]/div/div[1]/input').send_keys('123456')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[3]/div/button').click()
# 拼团
driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/div/span').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[9]/ul/li[1]').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button/span').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/form/div[1]/div/div/input[1]').click()
dangqin = time.strftime("%Y-%m-%d", time.localtime())
dangqin_two = time.strftime("%Y-%m-%d", time.localtime())
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[1]/div/input').send_keys(dangqin)
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input').send_keys(Keys.CONTROL + 'a')
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input').send_keys('00:00:00')
# test_time = driver.find_element_by_class_name('el-date-table')
# time_date = test_time.text
# n = time_date.split()
# print(n)
# print(dangqin)
# for time_dangqian in n:
#     if time_dangqian == dangqin:
#         print(time_dangqian)

# 5秒后关闭
sleep(5)
driver.quit()

