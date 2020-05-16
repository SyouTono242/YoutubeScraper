import requests
from bs4 import BeautifulSoup
import re

outputFile = open("output.txt","w")

listurl = 'https://www.youtube.com/playlist?list=PLiQ-AHFkVMznxM-NPbvtkVCQTR-8xXXI0'

data = requests.get(listurl)
data = data.text
soup = BeautifulSoup(data,"html.parser")

tr = soup.find_all("tr",class_="pl-video yt-uix-tile")
for element in tr:
    info = element.text.strip().split("\n")
    info = [x for x in info if not (x.isspace()or x=="")]
    title = info[0]
    channel = info[1].replace("by ","")
    videourl = "https://www.youtube.com/watch?v="+element["data-video-id"]
    length = info[2].strip()

    videoSoup = BeautifulSoup(requests.get(videourl).text, "html.parser")
    date = re.search(r'Published on(.*?)[\\]', str(videoSoup)).group(1).strip()

    print("【"+channel+"】"+title+"（"+date+"）")
    print(length)

