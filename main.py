import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_card_color_info(driver, data, is_sold_out):
    while True:
        try:
            print("загружаем страницу после клика")
            images_block = driver.find_element(By.ID, "experience-wrapper")
            print("загрузили")
            break
        except Exception as e:
            if "SBOX_FATAL_MEMORY_EXCEEDED" in str(e):
                driver.refresh()
    images_block1 = images_block.find_element(By.CLASS_NAME, "css-1rayx7p")
    buttons = images_block1.find_elements(By.CLASS_NAME, "css-du206p")

    photos = []
    for button in buttons:
        picture = button.find_elements(By.TAG_NAME, "picture")[1]
        img = picture.find_element(By.TAG_NAME, "img")
        href = img.get_attribute('src')
        photos.append(href)
        # print(href)
    data["photos"] = photos
    model_main_name = driver.find_element(By.XPATH, "//*[@id='pdp_product_title']")
    data["model_main_name"] = model_main_name.text
    # print(model_main_name.text)
    model_sub_name_block = driver.find_element(By.CSS_SELECTOR, '.d-lg-ib.mb0-sm.u-full-width.css-3rkuu4.css-1mzzuk6')
    model_sub_name = driver.find_element(By.CSS_SELECTOR, '.headline-5.pb1-sm.d-sm-ib').text
    data["model_sub_name"] = model_sub_name
    # print(model_sub_name)
    price = model_sub_name_block.find_element(By.CSS_SELECTOR,
                                              ".product-price").text
    data["price"] = price
    # print(price)
    coming_soon = driver.find_elements(By.CSS_SELECTOR, 'data-test="comingSoon"')
    is_coming_soon = len(coming_soon)
    if not is_sold_out and not is_coming_soon:
        sizes_block = driver.find_element(By.CSS_SELECTOR, ".mt5-sm.mb3-sm.body-2")
        active_sizes_inputs = sizes_block.find_elements(By.CSS_SELECTOR, "input:not([disabled])")
        sizes = []
        for input in active_sizes_inputs:
            input_id = input.get_attribute('id')
            size = sizes_block.find_element(By.CSS_SELECTOR, f"label[for='{input_id}']").text
            sizes.append(size)
            # (size)
        if not len(sizes):
            raise Exception("Размеры не спарсились")
        data["size"] = sizes


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


def get_card_info(driver, card_link, card_data):
    data = {}
    driver.get(card_link)
    colors = driver.find_elements(By.CSS_SELECTOR, ".css-b8rwz8.tooltip-component-container")
    articles = []
    for color in colors:
        color_input = color.find_element(By.NAME, "pdp-colorpicker")
        color_article = color_input.get_attribute('data-style-color')
        is_sold_out = color_input.get_attribute('data-nr-sold-out')
        # print(article)
        articles.append({"article": color_article, "is_sold_out": is_sold_out == 'true'})
    right_slash_index = card_link.rfind('/')
    base_link = card_link[:(right_slash_index + 1)]
    if len(colors) == 0:
        alone_article = card_link[(right_slash_index + 1):]
        articles.append({"article": alone_article, "is_sold_out": False})
    for article in articles:
        driver.get(base_link + article["article"])
        data["article"] = article["article"]
        # print(article)
        print(f"{article['article']}", article["article"])
        get_card_color_info(driver, data, article["is_sold_out"])
        print(f"{article['article']}", article["article"])
        card_data[f"{article['article']}"] = dict(data)


# Словарь с данными по карточке
data = {}
chrome_options = Options()
# неробот
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
cookie_allow(driver)
'''"https://www.nike.com/t/air-jordan-1-mid-se-mens-shoes-Zn07hL/DV1308-104",
    "https://www.nike.com/t/air-jordan-6-retro-mens-shoes-CVPFVM/CT8529-100",
    "https://www.nike.com/t/jordan-delta-2-se-shoes-ZpvFm3/DJ9843-004",
    "https://www.nike.com/t/air-jordan-1-low-mens-shoes-0LXhbn/553558-215",
    "https://www.nike.com/t/air-jordan-1-mid-mens-shoes-b3js2D/DQ8426-215",
    "https://www.nike.com/t/air-jordan-1-mid-se-mens-shoes-Zn07hL/DV1308-104",
    "https://www.nike.com/t/air-jordan-1-zoom-cmft-2-mens-shoes-Tw02qw/DV1307-060",
    "https://www.nike.com/t/air-jordan-7-retro-mens-shoes-098sXt/CU9307-106",
    "https://www.nike.com/t/air-jordan-7-retro-se-mens-shoes-8mRqbR/DN9782-001",
    "https://www.nike.com/t/air-jordan-xxxvii-low-basketball-shoes-00ZHpg/DV9909-401",
    "https://www.nike.com/t/air-jordan-11-retro-low-mens-shoes-4kj41D/AV2187-140",
    "https://www.nike.com/t/jordan-jumpman-team-ii-mens-shoe-GrWxfR/819175-106",
    "https://www.nike.com/t/air-jordan-1-low-se-mens-shoes-kMt2HL/DQ8422-001",
    "https://www.nike.com/t/air-jordan-1-retro-high-og-mens-shoes-VdpsB7/DZ5485-303",
    "https://www.nike.com/t/luka-1-next-nature-basketball-shoes-69X9Vs/DN1772-108",'''
card_links = [
    "https://www.nike.com/t/air-jordan-11-retro-low-mens-shoes-4kj41D/AV2187-140"

]
for card_link in card_links:
    print(card_link)
    card_data = {}
    get_card_info(driver, card_link, card_data)
    print(card_data)
    print(card_link, '\n\n')

driver.quit()
driver.close()
