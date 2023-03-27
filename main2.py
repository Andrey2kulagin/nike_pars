import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_phone_number(contact_block):
    try:
        phone_block = contact_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--phones-container--g5vgs")
        touch_phone_block = phone_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--phones_minimized--XieZH")
        touch_phone_block.click()
        phone_html = touch_phone_block.get_attribute("outerHTML")
        phone = phone_html[phone_html.find("tel:") + 4:]
        phone = phone[:phone.find('"')]
        print(phone)
        return phone
    except:
        print("Нет телефона")
        return "Нет телефона"


def get_email(contact_block):
    try:
        email_blocks = contact_block.find_elements(By.CLASS_NAME, "_3ea6fa5da8--socnetwork--Q6ec4")
        if len(email_blocks) > 1:
            for el in email_blocks:
                link_block = el.find_element(By.CLASS_NAME, "_3ea6fa5da8--socnetwork-icon--aUE0p")
                email_html = link_block.get_attribute("outerHTML")
                if email_html.find("mailto:") != -1:
                    email_block = el
                    break
        else:
            email_block = email_blocks[0]
        link_block = email_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--socnetwork-icon--aUE0p")
        email_html = link_block.get_attribute("outerHTML")
        email = email_html[email_html.find("mailto:") + 7:]
        email = email[:email.find('"')]
        print(email)
        return email
    except:
        print("Нет email")
        return "Нет email"


def get_fio(element2):
    name_block = element2.find_element(By.CLASS_NAME, "_3ea6fa5da8--title--OdkyF")
    name_block = name_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--agent-name--Q6y1w")
    name_block = name_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--name--JPPsh")
    print(name_block.text)
    return name_block.text


def get_agency(element2):
    information_blocks = element2.find_elements(By.CLASS_NAME, "_3ea6fa5da8--row--eMUih")
    agency_block = []
    for el in information_blocks:
        try:
            if el.find_element(By.CLASS_NAME, "_3ea6fa5da8--about-title--OCzbj").text == "Агентство":
                agency_block = el.find_element(By.CLASS_NAME, "_3ea6fa5da8--about-text--xx5UG").text
                break
            else:
                agency_block = "Нет информации об агентстве"
        except:
            continue
    print(agency_block)
    return agency_block


def get_region(element2):
    agency_information_block = element2.find_elements(By.CLASS_NAME, "_3ea6fa5da8--row--eMUih")
    region_block = []
    for el in agency_information_block:
        try:
            if el.find_element(By.CLASS_NAME, "_3ea6fa5da8--about-title--OCzbj").text == "Регион работы":
                region_block = el.find_element(By.CLASS_NAME, "_3ea6fa5da8--about-text--xx5UG").text
                break
            else:
                region_block = "Нет информации о регионе"
        except:
            continue
    print(region_block)
    return region_block


def get_experience(element2):
    experience_block = element2.find_element(By.CLASS_NAME, "_3ea6fa5da8--counters--YH7j7")
    year_experience_block = experience_block.find_element(By.CLASS_NAME, "_3ea6fa5da8--counters-item--kwGtk")
    year_experience_html = year_experience_block.get_attribute("outerHTML")
    position = year_experience_html.find("с 2")
    if position == -1:
        position = year_experience_html.find("с 1")
    year_experience = year_experience_html[position:position + 6]
    print(year_experience)
    return year_experience


def get_rating(element2):
    rating_bloke = element2.find_element(By.CLASS_NAME, "_3ea6fa5da8--rating-desctiption--HgRir")
    print(rating_bloke.text)
    return rating_bloke.text


def get_objects_in_work(element2):
    experience_block = element2.find_element(By.CLASS_NAME, "_3ea6fa5da8--counters--YH7j7")
    in_work_block = experience_block.find_elements(By.CLASS_NAME, "_3ea6fa5da8--counters-item--kwGtk")
    for el in in_work_block:
        text = el.text
        if text.find("В работе") != -1:
            out_str = text[text.find("В работе") + 9:]
        else:
            out_str = "Нет информации об объектах в работе"
    return out_str


def main_func(driver):
    out_str = ""
    element = driver.find_element(By.CLASS_NAME, "_3ea6fa5da8--container--bqTAG")
    element1 = element.find_element(By.CLASS_NAME, "_3ea6fa5da8--content--Q3iIo")
    element2 = element1.find_element(By.CLASS_NAME, "_3ea6fa5da8--main--xPGzo")
    fio = get_fio(element2)
    agency = get_agency(element2)
    region = get_region(element2)
    experience = get_experience(element2)
    rating = get_rating(element2)
    objects_in_work = get_objects_in_work(element2)
    # здесь сделать трай эксепт на нет контактов
    contact_block = element2.find_element(By.CLASS_NAME, "_3ea6fa5da8--container--j6vKU")
    phone_number = get_phone_number(contact_block)
    email = get_email(contact_block)
    print()
    cure_link = driver.current_url
    out_str = f"{fio};{email};{phone_number};{agency};{region};{experience};{rating};{objects_in_work};{cure_link}\n"
    return out_str


def get_pages_count(driver, link):
    driver.get(link)
    page_count = 1
    try:
        pages_count_block = driver.find_elements(By.CLASS_NAME, "_9400a595a7--content--sGuO7")
        for el in pages_count_block:
            page_count = el.text
        try:
            return int(page_count)
        except:
            print("WARNING!!! Получено не числовое значение кол-ва страниц")
    except:
        return page_count


chrome_options = Options()
# неробот
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="/home/andrey/PycharmProjects/parser_cian_1/chromedriver",
                          options=chrome_options)
regions_links = open("regions_links.txt", "r")

for link in regions_links:
    link_pattern = link[:link.find("page=") + 5]
    pages_count = get_pages_count(driver, link)
    print(link_pattern)
    for page_num in range(1, pages_count):
        print(page_num)
        cure_link = link_pattern + str(page_num)
        driver.get(cure_link)
        realtor_objects = driver.find_elements(By.CLASS_NAME, "_9400a595a7--container--J25nK")
        for realtor in realtor_objects:
            realtor.click()
            driver.switch_to.window(driver.window_handles[1])
            try:
                out_str = main_func(driver)
                output_file = open("output.txt", "a")
                output_file.write(out_str)
                output_file.close()
            except:
                pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

driver.close()
regions_links.close()
