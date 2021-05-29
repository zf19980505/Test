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
# 首页列表
tel_menu = driver.find_element_by_class_name('el-menu-vertical-demo').find_elements_by_xpath('li')
for menu_name in tel_menu:
    if menu_name.text == '活动管理':
        menu_name.click()
        module_el = menu_name.find_element_by_class_name('el-menu').find_elements_by_xpath('li')
        for module_name in module_el:
            if module_name.text == '拼团管理':
                module_name.click()
                break
        break
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/button').click()
new_group_lis = driver.find_element_by_class_name('el-form')
new_group_data = new_group_lis.find_elements_by_xpath('div')
print(len(new_group_data))


sleep(5)
driver.quit()

