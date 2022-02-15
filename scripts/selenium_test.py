from selenium import webdriver
from pyshadow.main import Shadow
import time

driver = webdriver.Chrome('chromedriver')
shadow = Shadow(driver)


driver.get("https://www.nytimes.com/games/wordle/index.html")
button = shadow.find_elements('.close-icon')
button[0].click()

keyboard = shadow.find_element('#keyboard')

word = 'hello'
for char in word:
    letter = shadow.find_element(keyboard, f'button[data-key="{char}"]')
    letter.click()

submit = shadow.find_element(keyboard, f'button[data-key="↵"]')
submit.click()
time.sleep(5)
driver.close()