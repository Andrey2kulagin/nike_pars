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


def do_pars(driver, link):
    print(link)
    driver.get(link)
    driver.set_window_size(1920, 1080)

    last_height = driver.execute_script("return document.body.scrollHeight")
    # Проматывание страницы до самого конца
    while True:
        # Cкроллим до конца страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ждем, пока страница загрузится
        time.sleep(3)

        # Вычисляем высоту страницы после скролла
        cards = driver.find_elements(By.CLASS_NAME, "product-card__img-link-overlay")
        new_height = driver.execute_script("return document.body.scrollHeight")
        count = driver.find_element(By.CSS_SELECTOR, ".wall-header__item_count").text
        if len(cards) == int(count.strip('()')):
            break
        last_height = new_height
    cards = driver.find_elements(By.CLASS_NAME, "product-card__img-link-overlay")
    print(len(cards))
    f = open("links.txt", 'a', encoding='utf-8')
    for card in cards:
        f.write(card.get_attribute('href') + '\n')
        print(card.get_attribute('href'))


chrome_options = Options()
# неробот
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
cookie_allow(driver)
links_file = open("links_for_link_pars.txt", 'r')
links = set(links_file.readlines())
links_len = len(links)
for link in links:
    print(links_len)
    links_len -= 1
    try:
        do_pars(driver, link)
    except Exception as e:
        print("Ошибка")
        f = open("links_gen_bags.txt", 'a')
        f.write("\n\nНачало бага\n")
        f.write(link)
        f.write(f"exception {e}")
        f.write(f"\n\n")
        f.close()
