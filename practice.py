import requests
from bs4 import BeautifulSoup

url = "https://blog.naver.com/bevak12/222618451669"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# rows = soup.find("p").get_text()
# rows = soup.find("div", attrs={"class":"se-main-container"})
nick = soup.find_all("span", attrs={"class":"nick"})
# row = nick[0].find("a").get_text()
# row = rows.find("span").get_text()

print(nick)
# print(row)
# for movie in movies:
#     title = movie.find("div", attrs={"class":"ImZGtf mpg5gc"}).get_text()
#     print(title)