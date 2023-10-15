from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id=177081285221-3irjc6filinptogbt1130jjte8n2n49n.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fnlle-b0128.firebaseapp.com%2F__%2Fauth%2Fhandler&state=AMbdmDm_77ceopADgcl9XYMBVbBcq7uRn6_qHiiLNRzO_w6ElLGO8F7BwS-YzaXyjmCBcP6e8acXKgP9AYHnEGq8CMGvq7vcow8vTjDtWZEQg-AvGXBff20i4Y_FK785a4QlWocsXRquz_BmXuDa_gM5xjKyAEBTB0weXiIKa8WyV5_M6RCrOiZT2j97L7FVcDvQES9fwfa7wYJZDO_VAVRPb8nEvY1fidRzpxmuHsqxpH7at9omEt8xhLvIYcdTvKuE8F7GeBuwkSiEvVDUY9fFQKx4TJaO3ML97hWNzzaRJSFYyT0e1CwBbi3b1e7bXsGnAWs&scope=openid%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20profile&context_uri=https%3A%2F%2Fwww.languagereactor.com&service=lso&o2v=1&theme=glif&flowName=GeneralOAuthFlow")
driver.find_element("xpath",'//input[@type="email"]').send_keys("tusabas12@gmail.com")
driver.find_element("xpath",'//*[@id="identifierNext"]').click()
time.sleep(3)
driver.find_element("xpath",'//input[@type="password"]').send_keys("")
driver.find_element("xpath",'//*[@id="passwordNext"]').click()
time.sleep(2)
driver.get('https://youtube.com')