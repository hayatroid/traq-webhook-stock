import os
import subprocess
import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/finance/quote/NI225:INDEXNIKKEI"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
price = soup.select(".YMlKec.fxKbKc")[0].contents[0]

message = f"【テスト】現在の日経平均株価は {price} 円です"
webhook_id = os.environ.get("WEBHOOK_ID")
subprocess.run(f'curl -X POST -H "Content-Type: text/plain; charset=utf-8" -d "{message}" https://q.trap.jp/api/v3/webhooks/{webhook_id}', shell=True)
