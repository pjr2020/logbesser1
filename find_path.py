import requests
from urllib import request
from bs4 import BeautifulSoup
import json
import csv

apache_repositories = ["flink","camel","lucene-solr","incubator-mxnet","spark"]
apache_repositories = ["apache/" + project for project in apache_repositories]

class github_crawl():

    def __init__(self):
        # 初始化一些必要的参数
        self.login_headers = {
            "Referer": "https://github.com/",
            "Host": "github.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
        }
 
        self.logined_headers = {
            "Referer": "https://github.com/login",
            "Host": "github.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
        }
 
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Authorization': 'token 35b515f23c17db11e21f1c4a26e3bfb2c39cbab2',#换上自己的token认证
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.login_url = "https://github.com/login"
        self.post_url = "https://github.com/session"
        self.session = requests.Session()
        self.filepaths = set()
 
    def parse_loginPage(self):
        # 对登陆页面进行爬取，获取token值
        requests.packages.urllib3.disable_warnings()
        html = self.session.get(url=self.login_url, headers=self.login_headers, verify=False)
        Soup = BeautifulSoup(html.text, "lxml")
        token = Soup.find("input", attrs={"name": "authenticity_token"}).get("value")
        
        return token
    # 获得了登陆的一个参数
 
    def login(self, user_name, password, keyword):
        # 传进必要的参数，然后登陆
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self.parse_loginPage(),
            "login": user_name,
            "password": password
        }
        
        logined_html = self.session.post(url=self.post_url, data=post_data, headers=self.logined_headers, verify=False)
        if logined_html.status_code == 200:
            self.parse_keyword(keyword)  # 获取了页面
 
    def parse_keyword(self, keyword):
        # 解析登陆以后的页面，筛选出包含这个关键字的java代码
        user_repositorys = set()  # 集合用来存放作者名和库名
        try:
 
            for i in range(11):
                url = "https://github.com/search?l=Java&p={id}&q={keyword}&type=Code".format(id=i+1, keyword=keyword)  # 循环的爬取页面信息
                resp = self.session.get(url=url, headers=self.login_headers, verify=False)
                soup = BeautifulSoup(resp.text, "lxml")
                pattern = soup.find_all('a', class_='text-bold')
 
                for item in pattern:
                    user_repositorys.add(item.string)
            for user_repository in user_repositorys:
                print(user_repository)
                self.get_results_from_keywords(user_repository, keyword)
 
        except Exception as e:
            print(e)
    
    def load_repositories(self, repositories):
        self.repositories = repositories
 
    def get_results_from_keywords(self, repository, keyword):  # 用Github的官方API爬取数据，解析json
        url = "https://api.github.com/search/code?q={keyword}+in:file+language:java+repo:{w}".format(w=repository, keyword=keyword)
        try:
            req = request.Request(url, headers=self.headers)
            response = request.urlopen(req).read()
            results = json.loads(response.decode())
            for item in results['items']:
                repo_url = item["repository"]["html_url"]
                file_path = item['html_url']
                self.loader_csv(repo_url, file_path, keyword)
 
        except Exception as e:
            print("获取失败",e)
            
    def loader_csv(self, repo_url, file_path, keyword):
        try:
            with open("path", "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([keyword, repo_url, file_path])
            csv_file.close()
        except Exception as e:
            print(e)
            
    def login_without_search(self, user_name, password, keywords):
        # 传进必要的参数，然后登陆
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self.parse_loginPage(),
            "login": user_name,
            "password": password
        }
        
        logined_html = self.session.post(url=self.post_url, data=post_data, headers=self.logined_headers, verify=False)
        if logined_html.status_code == 200:
            print("login success")
            for repository in self.repositories:
                for keyword in keywords:
                    self.get_results_from_local(repository, keyword)  # 获取了页面
                    
        self.loader_json()
            
    def get_results_from_local(self, repository, keyword):
        url = "https://api.github.com/search/code?q={keyword}+in:file+language:java+repo:{w}".format(w=repository, keyword=keyword)
        print("open url: " + url)
        try:
            req = request.Request(url, headers=self.headers)
            response = request.urlopen(req).read()
            results = json.loads(response.decode())
            for item in results['items']:
                file_path = item['html_url']
                self.filepaths.update(["https://raw.githubusercontent.com" + file_path[18:]])
 
        except Exception as e:
            print("获取失败",e)
            
    def loader_json(self):
        with open ("path.json", "w") as f:
            json.dump(self.filepaths, f)

x = github_crawl()
x.load_repositories(apache_repositories)
x.login_without_search("lmz16","limingzhe2016",["log.error", "log.info", "log.debug", "log.warn"])