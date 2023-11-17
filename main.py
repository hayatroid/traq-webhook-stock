from bs4 import BeautifulSoup
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
    ratio = ""
    stamp = ""
    try:
        ratio = soup.select(".si_i1_dl1 dd span")[1].contents[0].text
        if ratio[0] == "+":
            stamp = ":chart_with_upwards_trend:"
        else:
            stamp = ":chart_with_downwards_trend:"
        ratio = ratio[1:]
    except IndexError:
        ratio = soup.select(".si_i1_dl1 dd")[1].contents[0].text
        stamp = ":arrow_right:"
        ratio = ratio[:-1]
    message += f"|{name}|{price}|{ratio}% {stamp}|\n"

webhook_id = os.environ.get("WEBHOOK_ID")
headers = {"Content-Type": "text/plain; charset=utf-8"}
response = requests.post(f"https://q.trap.jp/api/v3/webhooks/{webhook_id}", headers=headers, data=message.encode("utf-8"))
print(message)
