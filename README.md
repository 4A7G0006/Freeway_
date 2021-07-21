# 開放式資料擷取


CWB_data.py :

CWB為交通部中央氣象局 網站開放資料下載

資料源 : https://opendata.cwb.gov.tw/index

將所有開放數據依照分類進行儲存 
(需安裝chrome & selenium & chromedriver.exe)

上交通部註冊可以獲得API授權碼 貼入code中Api_Key的地方 即可自動下載所有檔案


tisvcloud_data.py :

高速公路局即時資料庫資料下載

資料源 : https://tisvcloud.freeway.gov.tw/

只下載 (V2.0) 的資料

直接執行 即可下載所有即時資料(xml檔案)


tisvcloud_TDCS.py :

自動下載高公局的TDCS歷史資料

資料手冊 : https://tisvcloud.freeway.gov.tw/Sites/fyti/doc/TDCS%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8Av33.pdf

TDCS 歷史資料網站 : https://tisvcloud.freeway.gov.tw/history/TDCS

history weather.py:

將歷史天氣檔案下載下來

資料來源:https://e-service.cwb.gov.tw/HistoryDataQuery/

將檔案依照六都下載 時間與地點可修改程式設定 

#此程式碼目前都依照政府資料端網站實做
