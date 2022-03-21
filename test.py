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
# Display welcome message
Welcome()

# Get arti name and call Getsoup
name = input("请输入画师名字(如果不限画师 请输入: noname): \n")

soup = Getsoup(name)
path_name, page_numbers = Info_display(soup, name)
print("{} has {} page(s) of art on E621!".format(path_name, page_numbers))

#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#print(soup.prettify())

print("想要开始下载图片么，\n这样会在该目录中创建一个文件夹并且创建一个sub文件夹，以画师名字命名")
download_TF = str(input("[y/n]: \n"))
if download_TF.lower() == 'y':
    Downloader(path_name, page_numbers)
    print("下载完成！ \n")
else:
    print("输入非[ y ],取消下载. :3 ")
