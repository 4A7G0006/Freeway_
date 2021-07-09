import wget
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Api_Key = ""    # 請到https://opendata.cwb.gov.tw/userLogin 登入取得API授權碼後 填入


def create_folder(main_data, save_folder):
    if not os.path.exists(main_data):
        os.makedirs(main_data)
    for data in save_folder:
        data = main_data + '\\' + data
        if not os.path.exists(data):
            os.makedirs(data)


def catch_html(path, data_topic, data_page):
    driver = webdriver.Chrome("./chromedriver.exe")
    for get_topic, get_page in zip(data_topic, data_page):
        data = []
        for now in range(1, get_page + 1):
            driver.get("https://opendata.cwb.gov.tw/dataset/" + get_topic + "?page=" + str(now))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"content\"]/div/div/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/table/tbody/tr[2]"))
            )
            # time.sleep(5) #上面方法失效改用定時
            get_all = BeautifulSoup(driver.page_source, 'html.parser')
            closer = get_all.find('div').find('table', class_='table table-striped').find_all('td')
            for i in closer:
                word = i.text.split(' ')
                if len(word) > 1:
                    if word[1][0] == 'J':
                        data.append(word[0] + " " + word[1][0:4])
                    elif word[1][0] == 'Z' or word[1][0] == 'C' or word[1][0] == 'K' or word[1][0] == 'X':
                        data.append(word[0] + " " + word[1][0:3])
                    else:
                        data.append(i.text)
                if len(word) == 1 and word[0] != '':
                    data.append(word[0])
            # print(data)   #每個資料編號
            time.sleep(1)
        with open(path + '\\' + get_topic + ".txt", "w", encoding='utf-8-sig')as file:
            file.write("\n".join(data))
    driver.quit()


def download_data(path, topic, save_file):
    total_topic = []
    for names in topic:
        with open(path + '\\' + names + ".txt", "r", encoding='utf-8-sig')as file:
            lists = file.read().splitlines()
        total_topic.append(lists)

    for file_serial, files in enumerate(save_file):
        for data_serial, data in enumerate(total_topic[file_serial]):
            if data_serial % 2 == 0:
                content = data.rsplit(' ')[0]
                formats = data.rsplit(' ')[1]
            else:
                url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/" + data + "?Authorization=" + Api_Key + "&downloadType=WEB&format=" + formats
                new_path = path + '\\' + files + "\\" + content + ".json"  # 儲存的路徑
                print("\\" + content + ".json", end="")
                try:
                    wget.download(url, new_path)  # 下載
                    print(" Download Successful !")
                except:
                    print(" Download Failed !")
                    pass


name = r".\CWB_opendata"

save_file_folder = ['預測', '觀測', '地震海嘯', '氣候', '天氣警特報', '數值預報', '天文']  # 資料儲存用名稱
data_topic = ['forecast', 'observation', 'earthquake', 'climate', 'warning', 'mathematics', 'astronomy']  # 資料代號
data_page = [49, 15, 2, 4, 2, 32, 1]  # 資料頁數

# -----------test data----------------
'''
save_file_folder = ['天氣警特報', '天文']
data_topic = ['warning', 'astronomy']
data_page = [2, 1]
'''
# ------------------------------------

create_folder(name, save_file_folder)
catch_html(name, data_topic, data_page)
download_data(name, data_topic, save_file_folder)
