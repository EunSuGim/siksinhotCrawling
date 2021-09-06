import time
from pprint import pprint

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from Connect import *

class Search :

    def __init__(self):
        initpage()

    def searching(self):
        pprint("searching 시작")
        driver.find_element_by_css_selector('.focusIn').send_keys('오마카세')
        driver.find_element_by_css_selector('.focusIn').send_keys(Keys.ENTER)

        moreButton = driver.find_element_by_css_selector('div.listTy1 > a.btn_sMore')
        loop, count = True, 0

        while loop and count < 28:
            try:
                webdriver.ActionChains(driver).click(moreButton).perform()
                count += 1
                time.sleep(0.5)

            except TimeoutException:
                loop = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        restaurantsData = soup.select('div.listTy1 div.cont a')

        restaurantsInfo = [[data['href'], data.find('img')['src']] for data in restaurantsData]

        pprint("모든 가게 검색 준비완료")

        return restaurantsInfo

