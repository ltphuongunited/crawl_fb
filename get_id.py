from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException

def get_id(links):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=option)
    browser.get('https://findidfb.com')

    ID = []
    for lk in links:
        inputElement = browser.find_element_by_name("url_facebook")
        inputElement.send_keys(lk)
        sleep(random.randint(1,3))
        browser.find_elements_by_xpath("/html/body/div[1]/div[2]/div/form/p[2]/input")[0].click()
        try:
            id = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div[2]/div[1]/b").text
        except NoSuchElementException:
            id = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/b").text
        ID.append(id)
    
    browser.close()
    return ID


