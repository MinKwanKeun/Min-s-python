import requests
from bs4 import BeautifulSoup
import datetime as dt

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

def delete_iframe(url):
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml") 

    src_url = "https://blog.naver.com/" + soup.iframe["src"]
    
    return src_url

url1 = "https://blog.naver.com/starryspace/222626671980"
src_url1 = delete_iframe(url1)

now = dt.datetime.now()
# print(src_url1)

# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
res = requests.get(src_url1, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# print(soup)
rows = soup.find_all("p", attrs={"class":"se-text-paragraph se-text-paragraph-align-center"})
print("-"*50)
final_rows = []

for row in rows:
    rowrow = row.find("span").get_text()
    final_rows.append(rowrow)

# file_name = "{:%Y}".format(now.year)+"{:%m}".format(now.month)+"{:%d}.txt".format(now.day)
file_name = now.strftime("%Y")+ "_" + now.strftime("%m")+ "_" + now.strftime("%d")
f = open(file_name+".txt", "w", encoding="utf8")
for final_row in final_rows:
    if final_row[0] == "<" or final_row[0] == "-":
        continue
    elif final_row[0] == "​":
        f.write("\n")
    elif final_row[0] == '"':
        f.write("\n\n"+final_row[1:-1])
    else:
        f.write(final_row+" ")
        # if final_row[-1] == ".":
        #     f.write(final_row+" ")
        # else:
        #     f.write(final_row)
        # f.write(final_row)
f.close()