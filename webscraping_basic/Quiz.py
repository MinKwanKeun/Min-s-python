# Quiz) 부동산 매물(송파 헬리오시티) 정보를 스크래핑 하는 프로그램을 만드시오

# [조회 조건]
# 1. http://daum.net 접속
# 2. '송파 헬리오시티' 검색
# 3. 다음 부동산 부분에 나오는 결과 정보

# [출력 결과]
# =========== 매물 1 ===========
# 거래 : 매매
# 면적 : 84/59 (공급/전용)
# 가격 : 165,000 (만원)
# 동 : 214동
# 층 : 고/23
# =========== 매물 2 ===========
#   ...

# [주의 사항]
# - 실습하는 시점에 위 매물이 없다면 다른 곳으로 대체 가능

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re

class saving_list:
    def __init__(self, title='', bank='', interest_rate='', highest_interest_rate=''):
        self.title = title
        self.bank = bank
        self.interest_rate = interest_rate
        self.highest_interest_rate = highest_interest_rate

        print("이름 : " + self.title)
        print("은행 : " + self.bank)
        print("이자율 : " + self.interest_rate)
        print("최대 이자율 : " + self.highest_interest_rate)
        print(" ")

options = webdriver.ChromeOptions()

browser = webdriver.Chrome()
browser.maximize_window()

# 페이지 이동
url = "https://www.naver.com/"
browser.get(url)

soup = BeautifulSoup(browser.page_source, "lxml")

# 1. 검색창에 적금 입력
element = browser.find_element_by_name("query")
element.send_keys("적금")

# 2. 검색 버튼 클릭
elem = browser.find_element_by_id("search_btn")
elem.click()

# 3. 검색 소요시간 딜레이
# time.sleep(2)

# 4. 현재 url 주소 저장
url = browser.current_url
browser.get(url)

soup = BeautifulSoup(browser.page_source, "lxml")

total = soup.find("span", attrs={"class":"_total"}).get_text()

index = 0
p = re.compile("ca.e")
while True:
    current_page = soup.find("strong", attrs={"class":"npgs_now _current"}).get_text()

    print("============== {0} -> Page.[{1}] ================".format(type(current_page), current_page))

    if int(current_page) == int(total):
        savings = soup.find_all("strong", attrs={"class":"this_text"})
        banks = soup.find_all("span", attrs={"class":"text"})
        highest_interest_rates = soup.find_all("span", attrs={"class":"highest_txt"})
        
        f = open("information of saving.txt", "w", encoding="utf8")
        for saving in savings:
            saving = saving_list(savings[index].get_text(), banks[index*2].get_text(), banks[index*2+1].get_text(), highest_interest_rates[index].get_text())
            index += 1
            f.write("이름 : " + saving.title + "\n" + "은행 : " + saving.bank + "\n" + "이율 : " + saving.interest_rate + "\n" + "최대 이율 : " + saving.highest_interest_rate + "\n\n")
        f.close()

        print("다음 페이지가 없어 종료합니다.\n")
        break

    else:
        browser.find_element_by_xpath("//*[@id='main_pack']/section[1]/div[2]/div/div/div[3]/div/a[2]").click()
        print("\n '>' 버튼 클릭\n")
        index = 0

    soup = BeautifulSoup(browser.page_source, "lxml")

    print("다음 페이지로 넘어갑니다.\n")

browser.quit()