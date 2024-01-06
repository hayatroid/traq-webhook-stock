from bs4 import BeautifulSoup
from datetime import datetime
import os
from playwright.sync_api import sync_playwright
import requests
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y/%m/%d %H:%M")
message = f"""為替と株の値動きです ({now})
||現在値$\hspace{{5px}}$|前日比$\hspace{{8px}}$|
|:-:|-:|-:|
"""

html = ""
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://sekai-kabuka.com/")
    html = page.content()

soup = BeautifulSoup(html, "html.parser")
names = [":nikkei_heikin:", ":topix:", ":growth250:", ":sp500:", ":usd_jpy:", ":eur_jpy:"]
codes = ["NN0", "NN2", "NN4", "NN9", "NN14", "NN15"]
for name, code in zip(names, codes):
    price = soup.select(f"#{code} .怩侖鍠爲發隲蛞筵l穡倥")[0].contents[0].text
    ratio = soup.select(f"#{code} .亠搨ｰ臻l佩韆淅嚏l仄淪ｪN")[0].contents[0].text
    if code in ["NN14", "NN15"]:
        price, ratio = ratio, price
    stamp = ""
    if ratio[0] == "+":
        stamp = ":chart_with_upwards_trend:"
    elif ratio[0] == "-":
        stamp = ":chart_with_downwards_trend:"
    else:
        stamp = ":white_large_square:"
    message += f"|{name}|{price}|{ratio} {stamp}|\n"

webhook_id = os.environ.get("WEBHOOK_ID")
headers = {"Content-Type": "text/plain; charset=utf-8"}
response = requests.post(f"https://q.trap.jp/api/v3/webhooks/{webhook_id}", headers=headers, data=message.encode("utf-8"))
