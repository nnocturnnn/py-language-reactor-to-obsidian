from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get('https://quizlet.com/ru')
time.sleep(50)
button = driver.find_element("xpath","//button[@aria-label='Log in']")
button.click()
username_field = driver.find_element("id",'username')
password_field = driver.find_element("id"'password')

username_field.send_keys('your_username')
password_field.send_keys('your_password')

password_field.send_keys(Keys.RETURN)

time.sleep(5)

driver.quit()
