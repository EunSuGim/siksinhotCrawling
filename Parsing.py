import os

from Connect import *

import urllib.request
import os

from bs4 import BeautifulSoup
from pprint import pprint


class Parsing :

    '''
        데이터 파싱 작업 함수
        parameter : restaurantsInfo
        return : Array 결과값
    '''
    def parsingInfo(self, restaurantsInfo):

        pprint("parsing 시작")

        om = objectmanagements()

        results = []

        for info in restaurantsInfo :
            numbering =info[0].replace("/P/","")
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
            tellNumber =  soup.select_one('div.p_tel > p')
            holiday = soup.select_one('div.txt_holiday > dl > dd > span')
            parking = soup.select_one('li.info_li04')

            openTime = soup.select_one('ul.fLeft')

            if openTime:
                openingDay = openTime.select_one('span.tit')
                openingHour = openTime.select_one('label')
            else :
                openingDay = None
                openingHour = None


            slideImgTag = soup.select('div.slick-track > li > a')
            slideImg = [tmp.find('img')['src'] for tmp in slideImgTag]


            openingDay = om.exist(openingDay)
            openingHour = om.exist(openingHour)
            tellNumber = om.exist(tellNumber)
            holiday = om.exist(holiday)
            parking = om.existparking(parking)

            results.append(om.saveData(numbering,title,address,category,menuName,menuPrice,tellNumber,parking,holiday,openingDay,openingHour))

            om.imgDownload(info,slideImg)





        pprint("상세정보저장완료")

        return results



'''
   데이터 관리 클래스 
'''
class objectmanagements():

    '''
        데이터 저장 함수
        parameter : 저장할려는 데이터
        return : dict 결과값
    '''
    def saveData(self, numbering, title, address, category, menuName, menuPrice, tellNumber, parking, holiday,openingDay,openingHour):
        container = dict()

        container['numbering'] = numbering
        container['title'] = title
        container['address'] = address
        container['category'] = category
        container['menuName'] = menuName
        container['menuPrice'] = menuPrice
        container['tellNumber'] = tellNumber
        container['parking'] = parking
        container['holiday'] = holiday
        container['openingDay'] = openingDay
        container['openingHour'] = openingHour
        return container

    '''
        이미지 다운로드 함수
        parameter : 섬네일이미지정보, slide이미지정보
        return : None
    '''
    def imgDownload(self, info, slideImg):
        numbering =info[0].replace("/P/","")
        img =info[1]
        count = 1

        path = './data/image/{numbering}'.format(numbering=numbering)

        if not os.path.isdir(path) :
            os.makedirs(path)

        urllib.request.urlretrieve(img, './data/image/{numbering}/thumbnail.jpg'.format(numbering=numbering))

        for tmp in slideImg :
            urllib.request.urlretrieve(tmp, './data/image/{numbering}/slide_{count}.jpg'.format(numbering=numbering, count=count))
            count += 1


    '''
        None 데이터 정제 함수
        parameter : 정제할 데이터
        return : 정제된 데이터
    '''
    def exist(self, object):

        if object == None :
            object = "None"
        else :
            object = object.text

        return object

    '''
        주차여부판단 함수
        parameter : 주차데이터
        return : 정제된 데이터
    '''
    def existparking(self, object):

        if object != None:
            if "있음" in object.text:
                object = "o"
            else:
                object = 'x'
        else:
            object = 'None'

        return object
