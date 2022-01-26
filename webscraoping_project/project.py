# Project) 웹 스크래핑을 이용하여 나만의 비서를 만드시오

# [조건]
# 1. 네이버에서 오늘 서울의 날씨정보를 가져온다.
# 2. 헤드라인 뉴스 3건을 가져온다.
# 3. IT 뉴스 3건을 가져온다.
# 4. 해커스 어학원 홈페이지에서 오늘의 영어 회화 지문을 가져온다.

# [출력 예시]

# [오늘의 날씨]
# 흐림, 어제보다 OO˚ 높아요
# 현재 OO˚C (최저 OO˚ / 최고 OO˚)
# 오전 강수확률 OO% / 오후 강수확률 OO%

# 미세먼저 OO㎍/㎥ 좋음
# 초미세먼저 OO㎍/㎥ 좋음

# [헤드라인 뉴스]
# 1. 무슨 무슨 일이...
#  (링크 : http://...)
# 2. 어떤 어떤 일이...
#  (링크 : http://...)
# 3. 이런 저런 일이...
#  (링크 : http://...)

# [IT 뉴스]
# 1. 무슨 무슨 일이...
#  (링크 : http://...)
# 2. 어떤 어떤 일이...
#  (링크 : http://...)
# 3. 이런 저런 일이...
#  (링크 : http://...)

#  [오늘의 영어 회화]
#  (영어 지문)
#  Jason : How do you ....
#  Kim : Well, I think ....

# (한글 지문)
# Json : 어쩌구 저쩌구 ....
# Kim : 글쎄 ....

from attr import attr
import requests
from bs4 import BeautifulSoup
import re

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hQui8sp0J14ssQYtQLGssssssq4-047307"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

def scrape_weather(summary, now_temp, lowest_temp, highest_temp, rainfall_AM, rainfall_PM, micro_dust, super_micro_dust):
    print("[오늘의 날씨]")
    print(summary)
    print("현재 {0} (최저 {1} / 최고 {2})".format(now_temp, lowest_temp, highest_temp))
    print("오전 강수확률 {0} / 오후 강수확률 {1}".format(rainfall_AM, rainfall_PM))
    print(micro_dust)
    print(super_micro_dust)

class weather:
    def __init__(self, summary='', now_temp='', lowest_temp='', highest_temp='', rainfall_AM = '', rainfall_PM = '', micro_dust = '', super_micro_dust = ''):
        self.summary = summary
        self.now_temp = now_temp
        self.lowest_temp = lowest_temp
        self.highest_temp = highest_temp
        self.rainfall_AM = rainfall_AM
        self.rainfall_PM = rainfall_PM
        self.micro_dust = micro_dust
        self.super_micro_dust = super_micro_dust

temp_summary = soup.find("p", attrs={"class":"summary"}).get_text()
temp_now = str(soup.find("div", attrs={"class":"temperature_text"}).get_text())
temp_now = re.sub("현재 온도", "", temp_now)

temp_lowest = str(soup.find("span", attrs={"class":"lowest"}).get_text())
temp_lowest = re.sub("최저기온", "", temp_lowest)
temp_highest = str(soup.find("span", attrs={"class":"highest"}).get_text())
temp_highest = re.sub("최고기온", "", temp_highest)

rainfall_all = soup.find_all("span", attrs={"class":"rainfall"})
rainfall_AM = "0"
rainfall_PM = "0"
for index, rainfall in enumerate(rainfall_all):
    rainfall = str(rainfall_all[index].get_text())
    if index == 0:
        rainfall_AM = rainfall
    elif index == 1:
        rainfall_PM = rainfall
        break

micro_dust = soup.find("li", attrs={"class":"item_today level1"}).get_text()
micro_dust = re.sub("  ", "", micro_dust)
super_micro_dust = soup.find("li", attrs={"class":"item_today level3"}).get_text()
super_micro_dust = re.sub("  ", "", super_micro_dust)

weather_today = weather(temp_summary, temp_now, temp_lowest, temp_highest, rainfall_AM, rainfall_PM, micro_dust, super_micro_dust)

scrape_weather(weather_today.summary, weather_today.now_temp, weather_today.lowest_temp, weather_today.highest_temp, weather_today.rainfall_AM, weather_today.rainfall_PM, \
    weather_today.micro_dust, weather_today.super_micro_dust)

# ====================================================================================================

url = "https://news.naver.com/"
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

class news_class:
    def __init__(self, index, title, link):
        self.index = index
        self.title = title
        self.link = link

        print("{0}. {1}".format(self.index, self.title))
        print(" (링크 : {0})".format(self.link))

news = soup.select("div > div > section > div > div > div > div > div > div > div")

print("\n[헤드라인 뉴스]")
index = 0
for new in news:
    head_line_title = new.select_one("div.cjs_t")
    head_line_link = soup.select_one("a.cjs_news_a")["href"]
    # print(head_line_link)
    # print(type(head_line_title))
    if head_line_title == None:
        continue
    else:
        # new = news_class(head_line_title, head_line_link)
        # print(head_line_title.text)
        # print(head_line_link)
        index += 1
        new = news_class(index, head_line_title.text, head_line_link)
    if index == 5:
        break
# def head_line_news():


# [헤드라인 뉴스]
# 1. 무슨 무슨 일이...
#  (링크 : http://...)
# 2. 어떤 어떤 일이...
#  (링크 : http://...)
# 3. 이런 저런 일이...
#  (링크 : http://...)
