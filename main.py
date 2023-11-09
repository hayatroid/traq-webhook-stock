from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import os
import requests

data = []

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
    data.append(f"{name} : {price} ( !!:arrow_heading_{up_or_down}:!! {ratio[1:]}% )")

am_or_pm = ""
JST = timezone(timedelta(hours=+9), "JST")
if datetime.now(JST).hour < 12:
    am_or_pm = "おはよう！"
else:
    am_or_pm = "おつかれ！"

webhook_id = os.environ.get("WEBHOOK_ID")
headers = {"Content-Type": "text/plain; charset=utf-8"}
message = f"{am_or_pm}現在の株の値動きだよ！\n" + "　".join(data)
response = requests.post(f"https://q.trap.jp/api/v3/webhooks/{webhook_id}", headers=headers, data=message.encode("utf-8"))
