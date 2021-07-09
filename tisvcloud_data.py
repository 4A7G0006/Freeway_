import os
import wget
from bs4 import BeautifulSoup


def get_Serial():
    lists = []
    tisvclouds = "https://tisvcloud.freeway.gov.tw/"
    wget.download(tisvclouds, ".\index.html")
    with open("index.html", "r", encoding='utf-8-sig')as files:
        get_all = BeautifulSoup(files.read(), 'html.parser')
    table = get_all.find('table', class_='table style-1').find('tbody').find_all('tr')
    # print(table)
    for content in table:
        if content.find_all('td')[0].text[-6:] == "(v2.0)":
            save_data = content.find_all('td')[0].text + " " + content.find_all('td')[3].text + "\n" + tisvclouds[:-1] + content.find_all('a')[1].get('href')
            # print(save_data)
            lists.append(save_data)
    with open("freeway_data.txt", "w", encoding='utf-8-sig')as file:
        file.write("\n".join(lists))


def create_folder():
    save_path = ".\高工局資料"
    if os.path.exists(save_path):  # 資料夾是否存在
        pass
    else:
        os.makedirs(save_path)  # create new folder
        print("[ INFO: Create Folder Successful... ]")


def download_freeway_data():
    save_path = ".\高工局資料"
    with open("freeway_data.txt", "r", encoding='utf-8-sig')as file:
        list_all = file.read().splitlines()
    print(list_all)
    for n, s_file in enumerate(list_all):
        if n % 2 == 0:
            new_path = save_path + '\\' + s_file.rsplit(" ", 1)[0]
            if os.path.exists(new_path):  # 資料夾是否存在
                pass
            else:
                os.makedirs(new_path)  # create new folder
        else:
            print(new_path)
            path = new_path + '\\' + list_all[n - 1].rsplit(" ", 1)[0] + '.xml'
            print(new_path + '.\\' + list_all[n - 1].rsplit(" ", 1)[0] + '.xml', end="")
            wget.download(s_file, path)  # 下載
            print(" Successful")


create_folder()
get_Serial()
download_freeway_data()
