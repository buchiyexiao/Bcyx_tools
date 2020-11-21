import requests
import time
from bs4 import BeautifulSoup
import socket

url = None
page = 5

def scan_start():
    text = "ScanMan---Buchiyexiao\r\n"
    text+= "1 for subdomains\r\n"
    text+= "2 for hosts\r\n"
    text+= "3 for whois\r\n"
    text+= "help for get information for Scan_Man\r\n"
    text+= "99 for exit\r\n"
    print(text)
    while True:
        cmd = input("input>")
        if cmd == "help":
            help = "1 2 3-- use module\r\n"
            help+= "run\r\n"
            help+= "back\r\n"
        if cmd == "99":
            exit()
        if cmd == "1":
            url = None
            page = 5
            while True:
                domain = input('subdomains>')
                if domain == "show":
                    print("you can show options for more!")
                if domain == "exit":
                    exit()
                if domain == "show options":
                    print("domain:" + str(url) + "           |" + "type'set domain' to set the target\r\n")
                    print("pages:" + str(page) + "           |" + "type'set pages' to set the number you will get\r\n")
                if domain == "set domain":
                    url = input('set domain->')
                    print("You just have setted the domain as :" + str(url))
                if domain == "set pages":
                    page = int(input('set pages->'))
                    print("You just have setted the pages as :" + str(page))
                if domain == "back":
                    scan_start()

                if domain == "run":
                    if url == None:
                        print("Url is None\r\n")
                        scan_start()
                    if url != None:
                        print(url)
                        file = open('domainreport.txt','wb')
                        u = 'http://global.bing.com/search?q=site%3A'+url+'&qs=n&form=QBRE&sp=-1&pq=site%3A'+url+'&sc=2-11&sk=&cvid=C1A7FC61462345B1A71F431E60467C43'
                        headers = {
                            'User-Agent': 'ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400',
                            'Host': 'global.bing.com',
                            'Referer': 'http://global.bing.com/?FORM=HPCNEN&setmkt=en-us&setlang=en-us',
                            'Upgrade-Insecure-Requests': '1',
                            'Cache-Control': 'max-age=0',
                            'Connection': 'keep-alive',
                            'Cookie': 'DUP=Q=xa-EfMBM4gI7W690UHSTmQ2&T=312971513&A=2&IG=5161BB1CD80C4B8F8E04213C9A6BB2F1; MUID=35B121D519D96CA802AF2AE41DD96FD2; SRCHD=AF=HPCNEN; SRCHUID=V=2&GUID=59BB79AC0CDE4D8F853C004286CA05C4&dmnchg=1; SRCHUSR=DOB=20171201; MUIDB=35B121D519D96CA802AF2AE41DD96FD2; ULC=H=1D535|1:1&T=1D535|1:1; _RwBf=s=70&o=16; ipv6=hit=1512120707130&t=4; _EDGE_S=mkt=en-us&ui=en-us&SID=0AC562F3333D612722A469B832E160FE; SNRHOP=I=&TS=; _SS=SID=0AC562F3333D612722A469B832E160FE&HV=1512117115&R=0&bIm=473689; SRCHHPGUSR=CW=654&CH=997&DPR=1&UTC=480&WTS=63647713897'
                            }
                        for i in range(1, page):
                            data = {
                                'q': 'site:' + url,
                                'qs': 'n',
                                'sp': '3',
                                'sc': '0-12',
                                'sk': '',
                                'cvid': '710C7FF1A9B741C29D93EA4CCC435B27',
                                'first': i * 12,
                                'FORM': 'PERE'
                            }
                            sessions = requests.Session()
                            results = sessions.get(u, headers=headers, params=data)
                            soup = BeautifulSoup(results.content, 'html.parser')
                            job_bt = soup.findAll('h2')
                            for i in job_bt:
                                print(i.a.get('href'))
                                file.write((i.a.get('href')).encode('utf-8') + '\n'.encode('utf-8'))
                            time.sleep(3)
                        file.close()
                        scan_start()
        if cmd == "2":
            url = None
            while True:
                domain = input('hosts>')
                if domain == "show":
                    print("you can show options for more!")
                if domain == "exit":
                    exit()
                if domain == "show options":
                    print("domain:" + str(url) + "           |" + "type'set domain' to set the target\r\n")
                if domain == "set domain":
                    url = input('set domain->')
                    print("You just have setted the domain as :" + str(url))
                if domain == "back":
                    scan_start()
                if domain == "run":
                    if url == None:
                        print("Please set the target!")
                        scan_start()
                    if url != None:
                        f = open('DomaintoHosts.txt', 'w+')
                        myaddr = socket.getaddrinfo(url, 'http')
                        dst_ip = myaddr[0][4][0]
                        print(dst_ip)
                        f.writelines(dst_ip + ' ')
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
                        }
                        r = requests.get("https://www.shodan.io/host/" + dst_ip, headers=headers)
                        res = r.text
                        soup = BeautifulSoup(res, 'lxml')
                        result = soup.find_all(class_='ports')
                        a = str(result[0])
                        soupa = BeautifulSoup(a, 'lxml')
                        for i in soupa.find_all('a'):
                            print(i.get_text())
                            f.writelines(i.get_text() + ' ')
                        f.close()
                        scan_start()

        if cmd == "3":
            url = None
            while True:
                domain = input('whois>')
                if domain == "show":
                    print("you can show options for more!")
                if domain == "exit":
                    exit()
                if domain == "show options":
                    print("domain:" + str(url) + "           |" + "type'set domain' to set the target\r\n")
                if domain == "set domain":
                    url = input('set domain->')
                    print("You just have setted the domain as :" + str(url))
                if domain == "back":
                    scan_start()
                if domain == "run":
                    if url == None:
                        print("Please set the target!")
                        scan_start()
                    if url != None:
                        whoisheaders = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
                        }
                        whoisr = requests.get('http://whois.chinaz.com/' + url, headers=whoisheaders)
                        whoisres = whoisr.text
                        whoissoup = BeautifulSoup(whoisres, 'html.parser')
                        whoisa = whoissoup.find_all('p', class_="MoreInfo")
                        whoisresa = str(whoisa[0])
                        whoispresa = whoisresa.replace('<br/>', "\r\n")

                        whoisf = open('WhoisInfo.txt', "w+")
                        whoisf.write(whoispresa)
                        whoisf.close()
                        print(whoispresa)
                        scan_start()

if __name__ == '__main__':
    bcyx = scan_start()
