"""
    爬取梨视频首页视频
"""

import requests
from bs4 import BeautifulSoup
import re

url = "https://www.pearvideo.com/"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43",
    "Referer" : url
}
first_resp = requests.get(url, headers=headers)
first_resp.encoding = "utf-8"
main_page = BeautifulSoup(first_resp.text, "html.parser")
span_list = main_page.find("div", class_="act-main").find_all("span", class_="fav")
obj = re.compile(r'<span class="fav" data-id="(?P<id>.*?)">', re.S)
for span in span_list:
    id = obj.search(str(span)).group("id")
    url = f"https://www.pearvideo.com/video_{id}"
    contId = url.split("_")[1]
    videoStatusUrl = f"https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd=0.4185879253158611"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43",
        "Referer": url
    }
    resp = requests.get(videoStatusUrl, headers=headers)
    dic = resp.json()
    srcUrl = dic['videoInfo']['videos']['srcUrl']
    systemTime = dic['systemTime']
    srcUrl = srcUrl.replace(systemTime, f"cont-{contId}")
    with open(f"video/{contId}.mp4", mode="wb") as f:
        f.write(requests.get(srcUrl).content)
        print(f"{contId}.mp4 down!")
    resp.close()
first_resp.close()
print("over!")
