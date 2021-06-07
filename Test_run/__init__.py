from selenium import webdriver
from time import sleep
import random

driver = webdriver.Chrome()
driver.implicitly_wait(60)

driver.get('http://testback.3dshowarea.com/back/')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[1]/div/div/input').send_keys('ceshi4')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[2]/div/div[1]/input').send_keys('123456')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[3]/div/form/div[3]/div/button').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[10]/div').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/ul/li[10]/ul/li[1]').click()
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div[2]/button').click()

driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/form/div[1]/div/div/input').send_keys('测试优惠卷')
# 满多少减多少的这个钱随机生成0-1的两位数小数
full_money = random.uniform(0.0, 1.0)
full_money = round(full_money, 2)
subtract_money = random.uniform(0.0, full_money)
subtract_money = round(subtract_money, 2)
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/form/div[2]/div/div/input').send_keys(str(full_money))
driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/form/div[3]/div/div/input').send_keys(str(subtract_money))

driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/form/div[5]/div/div/div[1]/input').click()
test_li = driver.find_element('xpath', '/html/body/div[2]/div[1]/div[1]/ul').find_elements('xpath', 'li')
test_li_number = random.randint(0, len(test_li) - 1)
print('----------', len(test_li))
print('随机数：', test_li_number)
print(test_li[test_li_number].text)
sleep(2)
test_li[test_li_number].click()

sleep(5)
driver.quit()