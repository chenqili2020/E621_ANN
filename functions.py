from bs4 import BeautifulSoup
import requests
import os
import termcolor
import pyfiglet
import socket
import time
#pip install lxml


headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
url = 'https://e621.net/posts?tags='

def Welcome():
    f = pyfiglet.Figlet(font='standard')
    print("#" * 18, '\n')
    print(f.renderText('Welcome to EADBA!'))
    print("\n作者: 包子包.")
    print("#" * 18, '\n')

def Getsoup(name):
    """
    name = input("请输入画师名字(如果不限画师 请输入: noname): \n")
    """





    page = requests.get(url=url + name, headers=headers)
    # Forcing UTF-8
    page.encoding = "UTF-8"

    soup = BeautifulSoup(page.text, 'lxml')
    return soup

def Info_display(soup, name):
    """
    :param soup:
    :param name:
    :return: path_name, loop_num)
    """
    path_name = "xxx"
    loop_num = 0
    if name != "noname":
        post_list = soup.select('.user-disable-cropped-false  article ')
        while len(post_list) == 0:
            name = input("画师画作为0, 也许换个名字试一试? : \n")
            page = requests.get(url=url + name, headers=headers)
            # Forcing UTF-8
            page.encoding = "UTF-8"

            soup = BeautifulSoup(page.text, 'lxml')
            post_list = soup.select('.user-disable-cropped-false  article ')

        arts_num = soup.select('.category-1 > span')
        page_num = soup.select('.paginator  a')

        print("这个画师目前有 ", arts_num[0]["data-count"], " 作品在E621上.")

        # 打印基本消息

        if len(page_num) == 0:
            print("画师一共有 1 页")
            loop_num = 1
        else:
            print("一共有 ", page_num[-2].string, " 页数.")
            loop_num = int(page_num[-2].string)
        path_name = name

    else:
        name = ""
        print("输入为 不限制画师, 文件名字将显示为： “noname” \n")
        file_name = input("是否想自己命名文件夹?  Y/N: \n")
        valid_name = ["Y", "y", "N", "n"]
        while file_name not in valid_name:
            file_name = input("请输入 Y 或者 N : \n")
        if file_name == 'Y' or file_name == 'y':
            path_name = input("请输入文件名称: \n")

        else:
            path_name = "noname"

    return (path_name, loop_num)
    
def write_in_log(img_id, arti_name):
    """
    img_id: the post ID
    arti_name: the artist name
    This function write a txt file to record the downloaded art and artist name.
    """
    line = img_id+","+arti_name
    with open('horny_pics/download_log.txt', 'a') as f:
        f.write(line)
        f.write('\n')
    

def Downloader(arti_name, page_numbers):
    """
    """
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url_head = 'https://e621.net/posts?' + 'page='
    url_tail = '&tags=' + arti_name
    loop_num = page_numbers

    if not os.path.exists('./horny_pics' + '/' + arti_name):
        os.mkdir('./horny_pics' + '/' + arti_name)

    total_art = 0
    for num in range(0, loop_num + 1):
        url = url_head + str(num) + url_tail

        page = requests.get(url=url, headers=headers)
        page.encoding = "UTF-8"
        soup = BeautifulSoup(page.text, 'lxml')
        post_list = soup.select('.user-disable-cropped-false  article ')
        # 请求每一页的每张图
        print(len(post_list))
        for post in post_list:
            #set up the sleep time inorder to not get kicked out
            time.sleep(0.1)
            #print(post)
            
            #get some basic image info
            src = post['data-large-file-url']
            img_data = requests.get(url=src, headers=headers).content
            img_id = post['id']
            img_path = 'horny_pics/' + arti_name + '/'+arti_name + '_' + img_id + '.jpg'
            # 存图
            # TODO 加入更多的display 例如收藏数
            #print( "Downloading Art with ID {}, Up Vote{}, Fav Number {}")#.format(img_id,)
            total_art += 1
            
            # write the log txt
            # need to add check if it already created
            if os.path.exists('horny_pics/download_log.txt'):
                pass
            else:
                with open('horny_pics/download_log.txt', 'w') as log_txt:
                    log_txt.write("ID,Name")
                    log_txt.write("\n")
                
                
            # checking path and download
            if os.path.exists(img_path):
                print("Art {} already downloaded!".format(img_id))
            else:
                
                # write the binary img file
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)
                    print(img_id, "\nArt Download 完成！ >W< Art No.{}\n".format(total_art))
                    
                # write into log txt
                write_in_log(img_id, arti_name)


