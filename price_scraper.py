from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pip._vendor.distlib.compat import raw_input
import json
from product import Product
import time

URL = 'https://www.amazon.ae/'
# opts = Options()
# opts.set_headless()
driver = webdriver.Chrome()
driver.get(URL)

search_item = raw_input("what you want to search : ")

search = driver.find_element_by_id('twotabsearchtextbox')
search.send_keys(search_item)
search.send_keys(Keys.ENTER)
products = []


def convert_price_to_number(price):
    try:
        price = price.split("AED")[1]
        price = price.split("\n")[0] + "." + price.split("\n")[1]
    except:
        Exception()
    try:
        price = price.split(",")[0] + price.split(",")[1]
    except:
        Exception()
    return "AED", float(price)


page = 1
while True:
    if page != 1:
        try:
            driver.get(driver.current_url + "&page=" + str(page))
        except:
            break
    for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]'):

        counter = 0
        for element in i.find_elements_by_xpath('//div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/a'):
            should_add = True
            name = ''
            price = ''
            link = ''
            try:
                name = i.find_elements_by_tag_name('h2')[counter].text
                price = convert_price_to_number(element.find_element_by_class_name('a-price').text)
                link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")
            except:
                print('exception')
                should_add = False
            product = Product(name, price, link)
            if should_add:
                products.append(product)
            counter = counter + 1
    page = page + 1
    if page == 2:
        break
    print(page)

with open('{}_{}.json'.format(search_item, time.strftime("%Y_%m_%d")), 'w') as f:
    data = {
        'Products': [],
    }
    for i in products:
        data['Products'].append(i.serialize())
    json.dump(data, f, indent=4, sort_keys=True)
