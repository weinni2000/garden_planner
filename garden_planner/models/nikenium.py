from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests  # request img from web
import shutil  # save img locally
import re
import os
from pathlib import Path
from PIL import Image
import sys
import base64


def get_driver():
    server = True
    if sys.platform == 'win32':
        folder = "C:/temp/Chrome"
        server = False
    if sys.platform == "linux":
        folder = "/tmp/chromedata"
        pass
    else:
        folder = "data"

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir="+folder)
    if server:
        options.add_argument('--headless')
    # driver = webdriver.Chrome(
    #    "/Users/nikolaus.weingartmair/Desktop/Scripts/nikenium/driver/chromedriver", options=options)
    driver = webdriver.Chrome(
        executable_path='/opt/odoo15/odoo-custom-addons/garden_planner/helper/chromedriver/chromedriver', options=options)

    return driver


def test_google():
    driver = get_driver()
    driver.get("https://www.google.com")

    driver.title  # => "Google"

    driver.implicitly_wait(0.5)

    try:
        agree_button = driver.find_element_by_xpath(
            '//button[normalize-space()="Ich stimme zu"]')
        agree_button.click()
    except Exception as e:
        print(e)

    search_box = driver.find_element(By.NAME, "q")
    search_box = driver.find_element_by_xpath(
        "//input[contains(@title,'Suche')]")
    search_button = driver.find_element(By.NAME, "btnK")

    search_box.send_keys("Selenium")
    driver.implicitly_wait(0.5)
    search_button.click()

    driver.find_element(By.NAME, "q").get_attribute("value")  # => "Selenium"

    driver.quit()


def download_image(input):

    url = input["url"]
    url = "https://www.grueneerde.com/" + url
    folder = input["folder"]
    file_name = input["file_name"]

    res = requests.get(url, stream=True)

    folder = "./article_pictures/" + str(folder)
    Path(folder).mkdir(parents=True, exist_ok=True)

    if res.status_code == 200:
        with open(folder + "/" + file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', file_name)
    else:
        print('Image Couldn\'t be retrieved')

    im = Image.open(folder + "/" + file_name).convert("RGB")
    file_name = file_name.replace("webp", "png")
    im.save(folder + "/" + file_name, "png")


def get_flower_pictures(input):

    driver = get_driver()
    driver.get("https://www.google.com")

    driver.title  # => "Google"

    driver.implicitly_wait(0.5)

    try:
        agree_button = driver.find_element_by_xpath(
            '//button[normalize-space()="Ich stimme zu"]')
        agree_button.click()
    except Exception as e:
        print(e)

    search_box = driver.find_element(By.NAME, "q")
    search_box = driver.find_element_by_xpath(
        "//input[contains(@title,'Suche')]")
    search_button = driver.find_element(By.NAME, "btnK")

    search_button = driver.find_element_by_xpath(
        "//input[contains(@value,'Google Suche')]")

    search_box.send_keys(input["search_term"])
    driver.implicitly_wait(0.5)
    search_button.click()

    driver.implicitly_wait(1)

    bilder_button = driver.find_element_by_xpath(
        "//a[(text()='Bilder')]").click()
    """
    images = driver.find_elements_by_xpath(
        "//img[@jsname='Q4LuWd']")

    images = driver.find_elements(By.XPATH, "//img[@jsname='Q4LuWd']")
    """
    image_elements = driver.find_elements_by_css_selector(
        "img[jsname='Q4LuWd']")

    images = []
    for idx, image in enumerate(image_elements):
        if idx < 5:
            imagedict = {}
            src = image.get_attribute("src")
            imagedict["src"] = src
            imagedict["search_term"] = input["search_term"] + "_" + str(idx)

            imagedict = convert_to_file(imagedict)
            images.append(imagedict)
        else:
            break
    input["images"] = images

    driver.quit()

    return input


def convert_to_file(input):
    sample = 'data:image/jpeg;base64,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'

    m = re.search(r'data:image/(.+?);base64,(.+)', input["src"])
    fileextension = m.group(1)
    data = m.group(2)

    data_old = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADBQTFRFA6b1q Ci5/f2lt/9yu3 Y8v2cMpb1/DSJbz5i9R2NLwfLrWbw m T8I8////////SvMAbAAAABB0Uk5T////////////////////AOAjXRkAAACYSURBVHjaLI8JDgMgCAQ5BVG3//9t0XYTE2Y5BPq0IGpwtxtTP4G5IFNMnmEKuCopPKUN8VTNpEylNgmCxjZa2c1kafpHSvMkX6sWe7PTkwRX1dY7gdyMRHZdZ98CF6NZT2ecMVaL9tmzTtMYcwbP y3XeTgZkF5s1OSHwRzo1fkILgWC5R0X4BHYu7t/136wO71DbvwVYADUkQegpokSjwAAAABJRU5ErkJggg=='.replace(
        ' ', '+')

    data = data.replace(
        ' ', '+')

    input["src_string"] = data
    imgdata = base64.b64decode(data)

    input["src_decoded"] = data
    # I assume you have a way of picking unique filenames
    filename = input["search_term"] + '.jpg'
    folder = "./images/"
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(folder + filename, 'wb') as f:
        f.write(imgdata)

    return input


def get_ge_article_pictures():
    driver = get_driver()
    driver.get("https://www.grueneerde.com")
    driver.maximize_window()

    try:
        cookie_field = driver.find_element_by_xpath(
            '//a[normalize-space()="Alle Cookies akzeptieren"]')
        cookie_field.click()
    except Exception as e:
        print(e)

    articles = [76690]
    for article in articles:
        driver.implicitly_wait(0.5)
        # search_field = driver.find_element_by_xpath(
        #    '//input[@title="Bitte geben Sie hier den Suchbegriff ein!"]')

        # input[contains(@title,'Bitte geben Sie hier den Suchbegriff ein!')]/
        # search_field = driver.find_element_by_xpath(
        #    "//input[contains(@title,'Bitte geben Sie hier den Suchbegriff ein!') and @type='text']")
        search_field = driver.find_elements_by_css_selector(
            'li label input[type="text"].Required.ui-autocomplete-input')[1]

        # for f in search_field:
        #    print(f)
        # search_field = WebDriverWait(driver, 1).until(
        #    EC.element_to_be_clickable((By.CSS_SELECTOR, ".Watermark")))

        # getElementByXpath(input[contains(@title,'Bitte geben Sie hier den Suchbegriff ein!')]).innerHTML
        # working
        # document.evaluate('//input[contains(@title,"Bitte geben Sie hier den Suchbegriff ein!")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        id_search = search_field.get_attribute("id")

        print(id_search)
        value = article
        # document.querySelector('input.Required.ui-autocomplete-input').setAttribute('value','My default value')
        # document.querySelector("div.user-panel.main input[name='login']")
        # document.querySelector("div.user-panel.main input[name='login']")
        # document.getElementById("idc94").value = "My value"
        string = f"""document.getElementById('{id_search}').value='{value}'"""
        print(string)
        driver.execute_script(string)

        # driver.execute_script("arguments[0].click();", search_field)

        # document.evaluate('//input[contains(@title,"Bitte geben Sie hier den Suchbegriff ein!")]',
        #                  document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).value = "Johnny Bravo"
        # search_field = driver.find_element_by_xpath(
        #    "//li/label/input[contains(@class,'Watermark')]")
        # search_field = driver.findElement(
        #    By.xpath("//input[@title='Bitte geben Sie hier den Suchbegriff ein!']"))
        # search_field = driver.find_element(
        #    By.ID, "idcac")
        # search_field = driver.find_element_by_xpath(
        #    '//input[@class="Watermark"]')
        # driver.implicitly_wait(1)c
        # wait = WebDriverWait(driver, 1)
        # hover = ActionChains(driver).move_to_element(search_field)
        # hover.perform()

        # search_field.send_keys("76690")
        search_buttons = driver.find_elements_by_css_selector(
            'input[name="p::submit"]')[1]

        search_buttons.click()

        images = driver.find_elements_by_css_selector(
            'figure img[itemprop="image"]')

        for image in images:

            srcset = image.get_attribute("srcset")
            srcset_list = srcset.split(" ")

            url = srcset_list[0]

            # '/media/Image/imageOneOfTwelveWidth-webp/.fVuYaJoX/Image-243714/76690_imported.webp'
            m = re.search(r'.+/(.*?\.webp)', url)
            filename = m.group(1)

            input = {"url": url, "folder": article, "file_name": filename}
            download_image(input)

    print("end")


if __name__ == '__main__':
    #  test_google()
    input = {"search_term": "gänseblümchen"}
    get_flower_pictures(input)
    # get_ge_article_pictures()
