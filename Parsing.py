from Connect import *

import urllib.request

from bs4 import BeautifulSoup
from pprint import pprint


class Parsing :

    def parsingInfo(self, restaurantsInfo):

        pprint("parsing 시작")

        om = objectmanagements()

        results = []

        for info in restaurantsInfo :
            cd =info[0].replace("/P/","")
            img =info[1]
            connect(info[0])

            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            category = soup.head.find("meta",{"name" : "article:section3"}).get('content')
            if not "초밥" in category:
                continue

            title = soup.head.find("meta",{"name" : "dable:title"}).get('content')
            address = soup.head.find("meta", {"property" : "restaurant:contact_info:street_address"}).get('content')
            menuName = [menu.text for menu in soup.select("ul.menu_ul > li > span.tit")]
            menuPrice = [price.text for price in soup.select("ul.menu_ul > li > p > span > em > label")]
            phone =  soup.select_one('div.p_tel > p')
            holiday = soup.select_one('div.txt_holiday > dl > dd > span')
            parking = soup.select_one('li.info_li04')

            phone = om.exist(phone)
            holiday = om.exist(holiday)
            parking = om.existparking(parking)

            results.append(om.saveData(cd,title,address,category,menuName,menuPrice,phone,parking,holiday))

            urllib.request.urlretrieve(img,'./data/image/' + "{}.jpg".format(cd))




        pprint("상세정보저장완료")

        return results





class objectmanagements():

    def saveData(self, cd, title, address, category, menuName, menuPrice, phone, parking, holiday):
        container = dict()

        container['cd'] = cd
        container['title'] = title
        container['address'] = address
        container['category'] = category
        container['menuName'] = menuName
        container['menuPrice'] = menuPrice
        container['phone'] = phone
        container['parking'] = parking
        container['holiday'] = holiday

        return container



    def exist(self, object):

        if object == None :
            object = "모름"
        else :
            object = object.text

        return object

    def existparking(self, object):

        if object != None:
            if "있음" in object.text:
                object = "o"
            else:
                object = 'x'
        else:
            object = '모름'

        return object