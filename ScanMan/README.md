## Buchiyexiao的私人工具库（二）——渗透前期信息收集小工具

##### 菜鸡Bcyx

#### GITHUB https://github.com/buchiyexiao/Bcyx_tools

工具主要是对子域名和whois的一个搜索，功能性较差，还是建议使用在线搜索工具或者下载御剑等老牌工具，同时配备较为完善的字典进行扫描

### 收集域名信息

#### Whois查询

kali中默认安装Whois，只需要whois 域名比如whois baidu.com即可

一些在线的Whois查询网站由[爱站工具网](https;//whois.aizhan.com)，[站长之家](http://whois.chinaz.com)和[VirustTotal](https://www.virustotal.com)查询域名的服务商、拥有者等相关信息

#### 备案信息查询

国内网站的备案信息查询

主要是ICP备案查询网站：http://www.beianbeian.com，天眼查：http://www.tianyancha.com

### 收集敏感信息

Google的使用，借助clash-for-windows进行google的利用，一般google可以借助关键字进行搜索，Site（指定域名），Inurl（URL中存在关键字的网页），Intext（网页正文中的关键字），Filetype（指定文件类型），Intitle（网页标题中的关键字），link（link:baidu.com即表示返回所有和baidu.com做了链接的URL），Info(查找指定站点的一些基本信息)，cache（搜索Google中关于某些内容的缓存）

比如site:edu.cn intext:后台管理

也可以借助burp中的repeater功能得到一些服务器的信息，即抓包获取。

在获取到一些服务器和源代码的信息后，可以通过乌云漏洞表https://wooyun.shuimugan.com查询历史漏洞信息。

### 收集子域名信息

Layer子域名挖掘机

subDomainsBrute借助小字典进行递归寻找三级域名、四级域名等不容易发现域名

```
Usage: subDomainsBrute.py [options] target

Options:

  -h, --help            show this help message and exit

  -t THREADS_NUM, --threads=THREADS_NUM

                        Number of threads. default = 10

  -f NAMES_FILE, --file=NAMES_FILE

                        Dict file used to brute sub names

  -o OUTPUT, --output=OUTPUT

                        Output file name. default is {target}.txt
```

```
python subDomainsBrute.py -t 10 baidu.com --output text.txt
```

借助DNSdumpster网站https://dnsdumpster.com/，挖掘出指定域潜藏的大量子域

证书透明度CT是证书授权机构CA的一个项目，查找某个域名所属整数的最简单的方法就是使用搜索引擎搜索一些公开的CT日志

借助crt.sh https://crt.sh 和 censys https://censys.io 进行子域名枚举（identity like "%...."）

此外还有一些在线网站查询子域名，如子域名爆破网站https://phpinfo.me/domain和IP反查绑定域名网站http://dns.aizhan.com

### 手机常用端口信息

最常用的扫描工具就是Nmap

常见的端口及其说明以及攻击方向汇总如下

- 文件共享服务端口

  |  端口号  |       端口说明       |               攻击方向               |
  | :------: | :------------------: | :----------------------------------: |
  | 21/22/69 | Ftp/Tftp文件传输协议 | 允许匿名的上传、下载、爆破和嗅探操作 |
  |   2049   |       Nfs服务        |               配置不当               |
  |   139    |      Samba服务       |    爆破、未授权访问、远程代码执行    |
  |   389    |   Ldap目录访问协议   |      注入、允许匿名访问、弱口令      |

- 远程连接服务端口

  | 端口号 |    端口说明     |                    攻击方向                    |
  | :----: | :-------------: | :--------------------------------------------: |
  |   22   |       SSH       |     爆破、SSH隧道及内网代理转发、文件传输      |
  |   23   |     Telnet      |               爆破、嗅探、弱口令               |
  |  3389  | Rdp远程桌面连接 | Shift后门（windows server 2003以下系统）、爆破 |
  |  5900  |       VNC       |                   弱口令爆破                   |
  |  5632  | PyAnywhere服务  |                抓密码、代码执行                |

- Web应用服务端口

  |   端口号    |         端口说明          |             攻击方向              |
  | :---------: | :-----------------------: | :-------------------------------: |
  | 80/443/8080 |     常见的Web服务端口     | Web攻击、爆破、对应服务器版本漏洞 |
  |  7001/7002  |      WebLogic控制台       |       Java反序列化、弱口令        |
  |  8080/8089  | Jboss/Resin/Jetty/Jenkins |      反序列化、控制台弱口令       |
  |    9090     |      WebSphere控制台      |       Java反序列化、弱口令        |
  |    4848     |         GlassFish         |              弱口令               |
  |    1352     |   Lotus domino邮件服务    |      弱口令、信息泄露、爆破       |
  |    10000    |    Webmin-Web控制面板     |              弱口令               |

- 数据库服务端口

  |   端口号    |      端口说明      |           攻击方向           |
  | :---------: | :----------------: | :--------------------------: |
  |    3306     |       mysql        |       注入、提权、爆破       |
  |    1433     |    mssql数据库     |  注入、提权、爆破、SA弱口令  |
  |    1521     |    oracle数据库    |   TNS爆破、注入、反弹Shell   |
  |    5432     |  postgresql数据库  |      爆破、注入、弱口令      |
  | 27017/27018 |      MongoDB       |       爆破、未授权访问       |
  |    6379     |       Redis        | 可尝试未授权访问、弱口令爆破 |
  |    5000     | Sysbase/DB2 数据库 |          爆破、注入          |

- 邮件服务端口

  | 端口号 |   端口说明   |  攻击方向  |
  | :----: | :----------: | :--------: |
  |   25   | SMTP邮件服务 |  邮件伪造  |
  |  110   |   POP3协议   | 爆破、嗅探 |
  |  143   |   IMAP协议   |    爆破    |

- 网络常见协议端口

  | 端口号 |  端口说明   |               攻击方向                |
  | :----: | :---------: | :-----------------------------------: |
  |   53   | DNS域名系统 | 允许区域传送、DNS劫持、缓存投毒、欺骗 |
  | 67/68  |  DHCP服务   |              劫持、欺骗               |
  |  161   |  SNMP协议   |        爆破、搜集目标内网信息         |

- 特殊服务端口

  |   端口号    |        端口说明        |      攻击方向       |
  | :---------: | :--------------------: | :-----------------: |
  |    2181     |     Zookeeper服务      |     未授权访问      |
  |    8069     |       Zabbix服务       |  远程执行、SQL注入  |
  |  9200/9300  |   Elasticsearch服务    |      远程执行       |
  |    11211    |      Memcache服务      |     未授权访问      |
  | 512/513/514 |    Linux Rexec服务     |  爆破、Rlogin服务   |
  |     873     |       Rsync服务        | 匿名访问、文件上传  |
  |    3690     |        Svn服务         | Svn泄露、未授权访问 |
  |    50000    | SAP Management Console |      远程执行       |

### 指纹识别

御剑指纹识别或者一些在线网站查询CMS指纹识别，BugScaner：http://whatweb.bugscaner.com/look，云悉指纹：http://www.yunsee.cn/finger.html，WhatWeb：https://whatweb.net/

### 查找真实IP

如果不存在CDN，可以借助www.ip138.com获取目标的IP和域名信息

- 判断存在CDN（不同地点取最近）

  ping地址的时候地下显示出来的目标主域和上面不一致，也可以借助https://www.17ce.com等在线进行全国多地区ping

- 绕过CDN

  - 内部有相原
  - 扫描网站测试文件如phpinfo或test等
  - 分站域名
  - 国外访问 https://asm.ca.com/en/ping.php
  - 查询解析记录
  - 绕过CloudFlare CDN进行查找，http://www.crimeflare.us/cfs.html#box

### 收集敏感目录

御剑

