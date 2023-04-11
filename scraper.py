from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import lxml 

from bs4 import BeautifulSoup
import math
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def newTab():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

def closeTab():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def navigate(path, scroll=False):
    driver.get(path)
    if scroll:
        scrollSlowly()
    soup = BeautifulSoup(driver.page_source, "lxml")
    soup = BeautifulSoup(soup.prettify(), "lxml")
    return soup

def scrollSlowly():
    driver.execute_async_script(
            """
        count = 400;
        let callback = arguments[arguments.length - 1];
        t = setTimeout(function scrolldown(){
            console.log(count, t);
            window.scrollTo(0, count);
            if(count < (document.body.scrollHeight || document.documentElement.scrollHeight)){
              count+= 400;
              t = setTimeout(scrolldown, 1000);
            }else{
              callback((document.body.scrollHeight || document.documentElement.scrollHeight));
            }
        }, 100);"""
        )

pageCounter = 1
items = None


while (items != []):

    contents = navigate(f"https://ipon.hu/shop/csoport/szamitogep-alkatresz/alaplap/40?page={pageCounter}", True)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # sleep(5)

    items = contents.find_all("div", class_="shop-product")[0].find_all("a", class_ = "shop-card__overlay-link")

    print(f"page: {pageCounter}, lenOfArr: {len(items)}")

    for i in items:
        url = "https://ipon.hu" + i.get("href")
        newTab()
        contents = navigate(url)
        sleep(2)

        name = contents.find("h1", class_ = "product__title").contents[0].split("+ ")[0].replace("(Basic garancia)", "").strip()
        price = contents.find("div", class_="shop-card__price").contents[0].split("Ft")[0].replace(' ', '').strip()
        hungPrice = (math.ceil(int(price) * 0.31 * 0.9 / 500) * 500)
        image = contents.find("img", class_="product-gallery__image").get("src")

        string = f"{name} \n{hungPrice} \n{image} \n\n"
        print(string)
        with open("items.txt", "a", encoding="utf8") as f:
            f.write(string)

        closeTab()
    
    pageCounter += 1


driver.close()