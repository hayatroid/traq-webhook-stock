from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import os
import requests

message = """為替と株の値動きです
|指数名|現在値|前日比|
|-|-|-|
"""

codes = ["0000", "0010"]
for code in codes:
    url = f"https://kabutan.jp/stock/chart?code={code}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    name = soup.select(".si_i1_1 h2")[0].contents[1].text
    name = name.replace("日経平均", ":nikkei_heikin:")
    name = name.replace("ＴＯＰＩＸ", ":topix:")
    price = soup.select("span.kabuka")[0].contents[0].text
    ratio = soup.select(".si_i1_dl1 dd span")[1].contents[0].text
    up_or_down = ""
    if ratio[0] == "+":
        up_or_down = "up"
    else:
        up_or_down = "down"
    message += f"|{name}|{price}|{ratio[1:]}% :arrow_heading_{up_or_down}:|\n"

webhook_id = os.environ.get("WEBHOOK_ID")
headers = {"Content-Type": "text/plain; charset=utf-8"}
response = requests.post(f"https://q.trap.jp/api/v3/webhooks/{webhook_id}", headers=headers, data=message.encode("utf-8"))
