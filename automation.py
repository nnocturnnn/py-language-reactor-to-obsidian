from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from generator import generate_dictionary
from error import AppError
from utils import readInputText
import asyncio

def automation():
    # get title, description, and words from input.txt
    title, description, words = readInputText()

    #asynchronously get dictionary of word and definition pairs using openai api
    dictionary = asyncio.generate_dictionary(words)

    driver = webdriver.Chrome()
    driver.get("https://quizlet.com")


    # check if login button exists. If it exists wait until a user login successfully.
    login_button = driver.find_element(By.XPATH, "//div[@class='TopNavigation-contentRight']/div[2]/button")
    if login_button:                                                      
        login_button.click()
        #wait until it gets token cookie which indicates whethere a user is logged in.
        print("waiting for login in... (It might takes while after loged in please wait...)")
        driver.implicitly_wait(0)
        WebDriverWait(driver, 200).until(lambda driver: driver.get_cookie('AMZN-Token') != None)



    try:
        # go to create set and wait until it loads
        driver.get("https://quizlet.com/create-set")
        WebDriverWait(driver, 20).until(EC.url_contains("create-set"))
    except TimeoutException:
        #raise AppError if current set is a draft
        driver.quit()
        raise AppError("There might be a DRAFT set. Please SAVE YOUR DRAFT first and try again")


    #Close popup if it shows up
    close_pop_up = driver.find_elements(By. XPATH, "//div[@aria-label='Close modal']")
    if close_pop_up:
        close_pop_up[0].click()



    title_field = driver.find_element(By.XPATH ,"//input[@aria-label='Title']")
    description_field = driver.find_element(By.XPATH, "//textarea[@aria-label='Description']")
    # fill out title and description fileds
    title_field.send_keys(title)
    description_field.send_keys(description)

    # find and click word field of first row of a set
    input = driver.find_element(By.XPATH, "//div[@class='ProseMirror']")
    ActionChains(driver).click(input).perform()

    # count unreconizable english words 
    unkown_count = 0
    # each iteration fills out word and definition filed. Move pointer using TAB.
    for word, definition in dictionary.items():
        if definition.lower() == "unknown": unkown_count += 1
        time.sleep(0.1)
        ActionChains(driver).send_keys(word).send_keys(Keys.TAB).perform()
        time.sleep(0.2)

        ActionChains(driver).send_keys(definition).send_keys(Keys.TAB).perform()

        

    #set word and definition language to english
    language_bar = driver.find_elements(By.XPATH, "//div[@class='LanguageBarSide']/button")
    ActionChains(driver).click(language_bar[0]).send_keys('english').send_keys(Keys.ENTER).perform()
    ActionChains(driver).click(language_bar[1]).send_keys('english').send_keys(Keys.ENTER).perform()

    # click a create button
    submit = driver.find_elements(By.XPATH, "//button[@aria-label='Create']")[-1].click()

    print(f"Unkwon words: {unkown_count}\n")
    time.sleep(20)

    driver.quit()

asyncio.run(automation())