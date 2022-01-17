import csv
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # newline이 default가 enter인데, 그냥 공백으로 해서 줄을 깔끔하게 함(걍 냅두면 엔터 두 번, 저렇게 하면 엔터 한 번)
writer = csv.writer(f)

# resres = requests.get(url + str(1))
# resres.raise_for_status()
# row_soup = BeautifulSoup(resres.text, "lxml")
# data_data = row_soup.find_all("th")
# rowrow = [columnn.get_text().strip() for columnn in data_data]
# writer.writerow(rowrow)
title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t")
print(type(title))
writer.writerow(title)

for page in range(1, 5):
    res = requests.get(url + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미 없는 데이터는 skip
            continue
        data = [column.get_text().strip() for column in columns] # .strip() : /n/n/t/t/t/t 등 쓸데없는 것들 지움.
        # print(data)
        writer.writerow(data)