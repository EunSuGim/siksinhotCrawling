from selenium import webdriver

# 크롬 접속
driver = webdriver.Chrome("./driver/chromedriver.exe")
driver.implicitly_wait(3)

# webpage 불러오기

def initpage():
    driver.get("https://www.siksinhot.com/")
    print(driver.title)
    print(driver.current_url)

def connect(url):
    driver.get("https://www.siksinhot.com" + url)