import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os


listurl = 'https://www.youtube.com/playlist?list=PLiQ-AHFkVMznxM-NPbvtkVCQTR-8xXXI0'

filename = str(datetime.now().date()).replace("-","")[2::]+".txt"
f = open(filename, "a+")
if os.path.exists(filename) and os.stat(filename).st_size != 0:
    f.truncate(0)
data = requests.get(listurl)
data = data.text
soup = BeautifulSoup(data,"html.parser")

tr = soup.find_all("tr",class_="pl-video yt-uix-tile")

for idx, element in enumerate(tr):
    info = element.text.strip().split("\n")
    info = [x for x in info if not (x.isspace()or x=="")]
    title = info[0]
    channel = info[1].replace("by ","")
    videourl = "https://www.youtube.com/watch?v="+element["data-video-id"]
    length = info[2].strip()

    videoSoup = BeautifulSoup(requests.get(videourl).text, "html.parser")

    if re.search(r'Published on(.*?)[\\]', str(videoSoup)) is not None:
        date = re.search(r'Published on(.*?)[\\]', str(videoSoup)).group(1).strip()
        formatDate = datetime.strptime(date, "%b %d, %Y").date()
        date = str(formatDate).replace("-",".")
    else:
        date = "Error: date not found"

    if str(videoSoup).count("caption") != 0:
        caption = "有"
    else:
        caption = "无 提供mp3"

    print("加载到第"+str(idx+1)+"条视频: "+title)

    f.write("【"+channel+"】"+title+"（"+date+"）"+"\n")
    f.write(videourl+"\n")
    f.write("### "+"\n"+
            "游戏："+"\n"+
            "时长："+length+"\n"+
            "CC："+ str(caption)+"\n\n")
    sumVideo = idx+1
num_lines = sum(1 for line in f)
print("文件生成完毕√")
f.close()
