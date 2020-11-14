#encoding=utf-8
import urllib
import re
from bs4 import BeautifulSoup
import requests

class analysis:

    def __init__(self,dom,url):
        self.soup = BeautifulSoup(dom,'lxml')
        self.url = url

    def judge(self,link):
        if link == None:
            return False
        if link == '/':
            return False
        if link.find('javascript') == 0:
            return False
        return True

    def filter(self,link):
        if link.find('http') != 0:
            return self.url.rstrip('/') + "/" + link.lstrip('/')
        else:
            return link

    def _is_input_with_onclick(self, tag):
        return (tag.name == 'input') and (tag.get('type') == 'button') and tag.has_attr('onclick')

    def click_filter(self,link):
        pattern = re.compile("[\"'][ ]*\+[ ]*[\"']")
        return re.sub(pattern,'',link)

    def analysis_url(self):
        URL = []
        # URL_POST = []
        try:
            if 'utf-8' in self.soup.meta.get('content'):
                charset = 'utf-8'
            else:
                charset = 'gbk'
        except:
            charset = 'utf-8'

        for tag in self.soup.find_all('a'):
            if self.judge(tag.get('href')):
                URL.append(self.filter(tag.get('href')))

        for tag in self.soup.find_all('form'):
            if tag.get('method') == 'get':
                if tag.get('action'):
                    action_url = tag.get('action')
                else:
                    action_url = ''
                if self.judge(action_url):
                    action_url = self.filter(action_url)
                    param = []
                    for tag_tag in tag.find_all('input'):
                        if tag_tag.get('name') == None:
                            continue
                        value = ''
                        if tag_tag.get('value'):
                            value = tag_tag.get('value')
                        else:
                            value = 'admin'
                        value = value.encode(charset,'ignore')
                        param.append(tag_tag.get('name')+'='+urllib.quote(value))
                    URL.append(action_url + "?" + '&'.join(param))
            '''
            elif tag.get('method') == 'post':
                if tag.get('action'):
                    action_url = tag.get('action')
                else:
                    action_url = ''
                if self.judge(action_url):
                    action_url = self.filter(action_url)
                    param = []
                    for tag_tag in tag.find_all('input'):
                        if tag_tag.get('name') == None:
                            continue
                        value = ''
                        if tag_tag.get('value'):
                            value = tag_tag.get('value')
                        else:
                            value = 'admin'
                        value = value.encode(charset,'ignore')
                        param.append(tag_tag.get('name')+'='+urllib.quote(value))
                    URL_POST.append(action_url + "?" + '&'.join(param))
            '''
            for tag in self.soup.find_all(self._is_input_with_onclick):
                for i in re.findall(re.compile("href=([a-zA-Z0-9'\"+?=.%/_]*)"),tag.get("onclick")):
                    if self.judge(self.click_filter(i)):
                        URL.append(self.filter(self.click_filter(i)))

            #return URL,URL_POST
            return URL
