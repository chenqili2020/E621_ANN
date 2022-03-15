from bs4 import BeautifulSoup
import requests
import os
import termcolor
import pyfiglet
import socket
from functions import *
import time
# 设置socket层的超时时间为20秒
socket.setdefaulttimeout(20)

if not os.path.exists('./horny_pics'):
    os.mkdir('./horny_pics')
# 好看的打印
Welcome()

# Get arti name and call Getsoup
name = input("请输入画师名字(如果不限画师 请输入: noname): \n")

soup = Getsoup(name)
path_name, page_numbers = Info_display(soup, name)
print("{} has {} page(s) of art on E621!".format(path_name, page_numbers))

#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#print(soup.prettify())
Downloader(path_name, page_numbers)
