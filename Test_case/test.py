from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random


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
# driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button/span').click()
# 选中拼团商品
test_grpuds_tr = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/table/tbody'
                                               ).find_elements_by_xpath('tr')
for goouds_td in test_grpuds_tr:
    grouds = goouds_td.find_elements_by_xpath('td')
    print(grouds[3].text)
sleep(2)
driver.quit()

