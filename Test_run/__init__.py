from selenium import webdriver
from time import sleep
import random

driver = webdriver.Chrome()
driver.implicitly_wait(60)

driver.get('http://testback.3dshowarea.com/back/')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[1]/div/div/input').send_keys('ceshi4')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[2]/div/div[1]/input').send_keys('123456')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[3]/div/button').click()
# driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[10]/div').click()
# driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[10]/ul/li[1]').click()
# driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div[2]/button').click()
menu_path = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul').find_elements_by_xpath('li')
for menu_lis in menu_path:
    if menu_lis.text == '优惠券管理':
        sleep(1)
        menu_lis.click()
        modus = menu_lis.find_element_by_class_name('el-menu').find_elements_by_xpath('li')
        for modusname in modus:
            sleep(1)
            if modusname.text == '优惠券列表':
                modusname.click()
                break
        break

# menu_paths = driver.find_element_by_class_name('el-menu-vertical-demo').find_elements_by_xpath('li/div')
# for test_menu_lis in menu_paths:
#     if test_menu_lis.text == '优惠券管理':
test_ul = driver.find_element_by_class_name('el-menu').find_elements_by_xpath('li/ul/li')
for i in test_ul:
    if i .text == '优惠券发放':
        print(i.text)
        print('=========')

sleep(5)
driver.quit()