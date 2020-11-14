import re
import os
import sys
import sqlite3
import requests
import threading
import hashlib
from analysis import analysis

class Spiderman:

    def __init__(self,url):
        url = url.rstrip('/') + '/'
        self.tasks = [url]
        self.check = []
        self.conn = self.connectDB(url)
        self.ID = 0

    def match(self,id,url):
        url = url.rstrip('#')
        url = url.rstrip('&')
        url = url.rstrip('?')
        url = re.sub(re.compile("\d+"),'d+',url)
        text = hashlib.md5()
        text.update(url.encode("utf8"))
        mod_md5 = text.hexdigest()
        sql1 = "select ID from URLS where MD5=" + "'" + mod_md5 + "';"
        if len(self.conn.execute(sql1).fetchall()) > 0:
            return True
        else:
            self.ID += 1
            sql2 = "INSERT INTO URLS (ID,URL,MD5) VALUES (" + str(id) + ", '" + url + "', '" + mod_md5 + "');"
            self.conn.execute(sql2)
            self.conn.commit()
            return False

    def connectDB(self,url):
        text = hashlib.md5()
        text.update(url.encode("utf8"))
        file = text.hexdigest()
        if os.path.exists("./db/" + file + ".db3"):
            os.remove("./db/" + file + ".db3")
        else:
            pass
        conn = sqlite3.connect("./db/" + file + ".db3",check_same_thread=False)
        conn.execute('''CREATE TABLE URLS
        (ID INT PRIMARY KEY NOT NULL,
        URL TEXT NOT NULL,
        MD5 TEXT NOT NULL);''')
        return conn

    def judge(self):
        return (not self.tasks)

    def start(self,url):
        try:
            dom = requests.get(str(url))
            dom = dom.content.decode('utf-8')
            Handle = analysis(dom,url)
            return Handle.analysis_url()
        except:
            return []

    def spider(self,urls):
        if urls:
            for url in urls:
                url = url[0:url.rfind('/')]
                if self.start(url):
                    self.check += self.start(url)
        return self.check

    def spiderman(self):
        while not self.judge():
            self.spider(self.tasks)
            self.tasks = []
            for u in  self.check:
                if not self.match(self.ID,u):
                    self.tasks.append(u)
                else:
                    pass
            self.check = []
        print("End!!!!")
        print("End!!!!")
        print("End!!!!")
        print("End!!!!")
        self.conn.close()

if __name__ == '__main__':
    url = 'http://demo.aisec.cn/demo/aisec/'
    Spiderman(url).spiderman()