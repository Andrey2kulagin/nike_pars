import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# неробот
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.nike.com/t/air-jordan-2-retro-low-mens-shoes-LVlsNr/DV9956-118")
time.sleep(5)
print(driver)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                     "nds-dialog__actions")))

element.click()
wait = WebDriverWait(driver, 10)
#driver.refresh()
images_block = wait.until(EC.presence_of_element_located((By.ID, "experience-wrapper")))
images_block1 = images_block.find_element(By.CLASS_NAME, "css-1rayx7p")
buttons = images_block1.find_elements(By.CLASS_NAME, "css-du206p")
for button in buttons:
    picture = button.find_elements(By.TAG_NAME, "picture")[1]
    img = picture.find_element(By.TAG_NAME,"img")
    href = img.get_attribute('src')
    print(href)
info_block = driver.find_element(By.ID, "RightRail")
print(info_block.get_attribute('innerHTML'))
all_info_block = info_block.find_element(By.CLASS_NAME, "prl0-sm.mb8-sm")
name_block1 = driver.find_elements(By.XPATH, "//*[@id='pdp_product_title']")

for el in name_block1:
    print(el.get_attribute('innerHTML'))






