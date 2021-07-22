import os
import wget
from bs4 import BeautifulSoup
import tarfile
import shutil

#------------------------------------
'''
檔案較大下載大約需花上三天
解壓縮的部分也順便寫好
總共跑完大約需花上一個多星期不等--
'''
#------------------------------------
def makedir_s(names):
    path = names
    if os.path.exists(path):  # 資料夾是否存在
        pass
    else:
        os.makedirs(path)  # create new folder
        os.makedirs(path + '\\' + "total_data")
        os.makedirs(path + '\\' + "time_list")
        print("[ INFO: Prepare folder create Successful... ]")


def get_freeway_data(names):
    lists = []
    path = names + '\\'
    freeway_data = "https://tisvcloud.freeway.gov.tw/history/TDCS"
    wget.download(freeway_data, path + "data.html")
    with open(path + "data.html", "r", encoding='utf-8-sig')as files:
        get_all = BeautifulSoup(files.read(), 'html.parser')
    table = get_all.find('table', class_='table style-1').find('tbody')
    for content in table.find_all('a')[:0:-1]:
        temp = content.text + "\n" + freeway_data + "/" + content.text + "/"
        lists.append(temp)
    with open(path + "maindata.txt", "w", encoding='utf-8-sig')as file:
        file.write("\n".join(lists))


def download_html(path):
    html_path = path + '\\' + "total_data"
    with open(path + '\\' + "maindata.txt", "r", encoding='utf-8-sig')as file:
        list_all = file.read().splitlines()
    # print(list_all)
    for n, s_file in enumerate(list_all):
        if n % 2 == 0:
            if os.path.exists(path + '\\' + s_file):  # 資料夾是否存在
                pass
            else:
                new_path = path + '\\' + s_file
                os.makedirs(new_path)  # create new folder
                # print(new_path + " folder create Successful")
        else:
            path_download = html_path + '\\' + list_all[n - 1] + '.html'
            print(html_path + '\\' + list_all[n - 1] + '.html', end="")
            try:
                wget.download(s_file, path_download)  # 下載
                print(" Successful")
            except:
                print(" Failed")
                pass


def catch_Serial(path):
    html_path = path + '\\' + "total_data"
    save_word = path + '\\' + "time_list"
    all_file = os.listdir(html_path + '\\')
    for text in all_file:
        lists = []
        position = html_path + '\\' + text
        with open(position, "r", encoding='utf-8-sig')as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
        table = soup.find('table', class_='table style-1').find('tbody')
        for content in table.find_all('a')[1:]:
            print(content.text)
            lists.append(content.text)
        with open(save_word + '\\' + text[:-5] + ".txt", "w", encoding="utf-8-sig")as file:
            file.write("\n".join(lists))


def get_file(path):
    all_folder = []
    all_gz = []
    times = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']  # 一天的小時數
    mins = ['0000', '0500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000', '5500']  # 每小時內的時間
    with open(path + '\\' + "maindata.txt", "r", encoding='utf-8-sig')as file_s:
        link_all = file_s.read().splitlines()[1::2]
    with open(path + '\\' + "maindata.txt", "r", encoding='utf-8-sig')as file_m:
        file_all = file_m.read().splitlines()[::2]
    waydata_path = path + '\\' + "time_list" + '\\'
    waydatas = os.listdir(waydata_path)
    for alone in waydatas:
        folder = []
        gz = []
        with open(waydata_path + alone, "r", encoding='utf-8-sig')as get:
            All_data = get.read().splitlines()
        for data in All_data:
            if data[-3:] == ".gz":
                gz.append(data)
            else:
                folder.append(data)
        all_folder.append(folder)
        all_gz.append(gz)
    for n, out in enumerate(link_all):
        print("dir file start download--------------")
        for mid in all_folder[n]:
            new_path = path + '\\' + file_all[n] + '\\' + mid
            if os.path.exists(new_path):  # 資料夾是否存在
                pass
            else:
                os.makedirs(new_path)  # create new folder
                print(new_path + " Folder create Sucessful")
            link_path = out + mid + '/'  # ''' https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20210708/'''
            print("-GET " + link_path)
            for time_s in times:
                new_path_1 = new_path + '\\' + time_s
                if os.path.exists(new_path_1):  # 資料夾是否存在
                    pass
                else:
                    os.makedirs(new_path_1)  # create new folder
                    print(new_path_1 + " folder create Sucessful")
                for min in mins:
                    link_path1 = link_path + time_s + '/' + "TDCS_" + file_all[n] + "_" + mid + "_" + time_s + min + ".csv"
                    print("--GET " + link_path1)
                    # https: // tisvcloud.freeway.gov.tw / history / TDCS / M03A / 20210708 / 17 / TDCS_M03A_20210708_174000.csv
                    savepath = new_path_1 + "\TDCS_" + file_all[n] + "_" + mid + "_" + time_s + min + ".csv"
                    if not os.path.exists(savepath):
                        try:
                            wget.download(link_path1, savepath)
                            print("---" + "TDCS_" + file_all[n] + "_" + mid + "_" + time_s + min + ".csv" + "   Download Successful!")
                        except:
                            print("---" + "TDCS_" + file_all[n] + "_" + mid + "_" + time_s + min + ".csv" + "   Download Failed!")
                            pass
                    else:
                        print("Pass")
                        pass
        print(".gz file start download--------------")
        for gz_files in all_gz[n]:
            link = link_all[n] + gz_files
            print(link)
            print("---" + gz_files)
            new_save = path + '\\' + file_all[n] + '\\' + gz_files
            if not os.path.exists(new_save):
                try:
                    wget.download(link, new_save)
                    print("    Successful")
                except:
                    print("    Failed")
            else:
                print("PASS")
                pass


def tar_extract(file_path, name):  # 檔案解壓縮
    tar = tarfile.open(file_path + '\\' + name, 'r:gz')
    print("extract file -- " + name)
    tar.extractall(path=file_path)


def gz_file_ex(path):
    with open(path + '\\' + "maindata.txt", "r", encoding='utf-8-sig')as file_m:
        file_all = file_m.read().splitlines()[::2]
    for file in file_all:
        ex_path = path + '\\' + file
        allfile = os.listdir(ex_path)
        for item in allfile:
            if item[-7:] == ".tar.gz":
                tar_extract(ex_path, item)
                os.remove(ex_path + '\\' + item)
                print("-remove " + item)
        deep_path = ex_path + '\\' + file
        deep_file = os.listdir(deep_path)
        for deep in deep_file:
            if not os.path.exists(ex_path + '\\' + deep):
                shutil.move(deep_path + '\\' + deep, ex_path + '\\' + deep)
                print(deep + " File move exactly")
        if os.path.exists(deep_path):
            shutil.rmtree(deep_path)
        print("remove folder:" + deep_path)


if __name__ == '__main__':  # 主程式在這
    name = "F:\\Data"  # input folder name or folder path
    makedir_s(name)
    get_freeway_data(name)
    download_html(name)
    catch_Serial(name)
    get_file(name)
    gz_file_ex(name)

