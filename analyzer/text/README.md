
# 文字情緒分析介紹
> natural_lang_process  
> 透過Cloud Natural Language API進行情緒分析  
> 要有Google Cloud的帳戶服務才能使用
> 請先看API憑證設置說明，照上面的步驟設置好憑證    
-------------------------------------------------------------------------------
# API憑證設置說明
## 建立帳號
> 1.先在 https://console.cloud.google.com/freetrial?authuser=1&_ga=2.212849623.-2134781270.1533114916   
>   建立自己的Google Cloud的帳號方案（需綁定信用卡）  
> 2.建立完後會有300美金，12個月的試用額度能用，  
    可在 https://console.cloud.google.com/home/dashboard 觀看自己的使用情況和管理專案  
    
## 前置環境安裝 Google Cloud SDK
> 1.到 https://cloud.google.com/sdk/docs/quickstart-windows 下載 Google Cloud SDK installer  
> 2.安裝完畢後，照上面指示登入google帳號，並選擇使用的project  

## 憑證設置
> 1.先在 https://console.cloud.google.com/apis/credentials 建立憑證  
> 2.下載憑證的json檔  
> 3.打開 cmd  
> 4.輸入 set GOOGLE_APPLICATION_CREDENTIALS=[PATH]  
    [PATH]為你憑證放置路徑（須包含檔名）  
-------------------------------------------------------------------------------

# 功能介紹
## text_analyze(text) 
> 丟文字進去text_analyze()函數，會回傳-1~1的情緒分數  

