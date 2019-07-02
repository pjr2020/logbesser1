import requests
from urllib import request
from bs4 import BeautifulSoup
import json
import datetime
import os

login_headers = {
    "Referer": "https://github.com/",
    "Host": "github.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
    }
 
logined_headers = {
    "Referer": "https://github.com/login",
    "Host": "github.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
    }
 
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'token 35b515f23c17db11e21f1c4a26e3bfb2c39cbab2',#换上自己的token认证
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

login_url = "https://github.com/login"
post_url = "https://github.com/session"
session = requests.Session()

requests.packages.urllib3.disable_warnings()
html = session.get(url=login_url, headers=login_headers, verify=False)
Soup = BeautifulSoup(html.text, "lxml")
token = Soup.find("input", attrs={"name": "authenticity_token"}).get("value")

post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": token,
            "login": "lmz16",
            "password": "limingzhe2016"
        }
logined_html = session.post(url=post_url, data=post_data, headers=logined_headers, verify=False)

with open("path.json", "r") as f:
    paths = json.load(f)
    count = 0
    for path in paths:
        path = path.replace("blob/", "")
        print(path)
#         req = request.Request(path, headers=headers)
#         content = request.urlopen(req).read().decode('utf8').split("\n")
        try:
            content = requests.get(path, login_headers).text.split("\n")
        except Exception as e:
            print(e)
        if not (os.path.exists(str(datetime.date.today().strftime("%d%m%Y")))):
            os.mkdir(str(datetime.date.today().strftime("%d%m%Y")))
        with open(str(datetime.date.today().strftime("%d%m%Y")) + "/" + str(count) + ".java", "w") as f_:
            for line in content:
                f_.writelines(line + "\n")
        count = count + 1