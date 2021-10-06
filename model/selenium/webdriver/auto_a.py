
from  selenium import webdriver
from time import sleep
driver = webdriver.Chrome()

# 访问指定的url
driver.get('http://ww.baidu.com')


# 输入
driver.find_element_by_id('kw').send_keys("测试")

#点击 百度一下按钮

driver.find_element_by_id('su').click()

#等待
sleep(2)

#点击第一条连接
driver.find_element_by_xpath('//*[@id="1"]/h3/a').click()