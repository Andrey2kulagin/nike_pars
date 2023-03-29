import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def cookie_allow(driver):
    card_link = "https://www.nike.com/t/air-jordan-1-mid-se-mens-shoes-Zn07hL/DV1308-104"
    driver.get(card_link)
    while True:
        try:
            print("пробуем кликнуть")
            time.sleep(3)
            element = driver.find_element(By.CLASS_NAME, "nds-dialog__actions")
            element.click()
            print("кликнули")
            break
        except:
            driver.refresh()


chrome_options = Options()
# неробот
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
cookie_allow(driver)
links = [
    "https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok"
]
for link in links:
    print(link)
    driver.get(link)
    driver.set_window_size(1920, 1080)

    last_height = driver.execute_script("return document.body.scrollHeight")
    # Проматывание страницы до самого конца
    cards = 0
    while True:
        # Cкроллим до конца страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ждем, пока страница загрузится
        time.sleep(3)

        # Вычисляем высоту страницы после скролла
        cards = driver.find_elements(By.CLASS_NAME, "product-card__img-link-overlay")
        new_height = driver.execute_script("return document.body.scrollHeight")
        count = driver.find_element(By.XPATH, "//*[@id='Mens-Jordan-Shoes']/span").text
        if len(cards) == int(count.strip('()')):
            break
        last_height = new_height
    cards = driver.find_elements(By.CLASS_NAME, "product-card__img-link-overlay")
    print(len(cards))
    f = open("links.txt", 'a', encoding='utf-8')
    for card in cards:
        f.write(card.get_attribute('href') + '\n')
        print(card.get_attribute('href'))
