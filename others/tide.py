from bs4 import BeautifulSoup
import requests
import time

#日期格式化
d = time.strftime("%Y-%m-%d", time.localtime())
#print (d)
#获取数据
html = requests.get("http://www.chinaports.com/chaoxi/" + d + "/122").content
soup = BeautifulSoup(html, "html5lib", from_encoding="utf-8")
result = soup.find("table", class_="tidaltable")
detail = result("td")
#print (detail)

count = len(detail)
#print (result.descendants)

s = ""
for child in detail:
    s = s + child.string + " "
#    print (child.string)
#print (s)

if count == 8:
    tide_time = s[0:20]
    tide_height = s[28:]
    print (tide_time)
    print ("潮高 " +tide_height)
else:
    tide_time = s[0:26]
    tide_height = s[35:]
    print (tide_time)
    print ("潮高 " + tide_height)



