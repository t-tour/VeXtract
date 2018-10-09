## ffmepg環境設定
> 1.先到這個網頁 https://jsnwork.kiiuo.com/archives/2705/ffmpeg-windows-%E5%AE%89%E8%A3%9D/  
> 2.照上面的說明安裝ffmpeg，並設定環境變數  
> 3.檔案若非在執行的根目錄底下，就要輸入檔案的完整路徑（路徑不要加"" or ''）

# 主要功能說明
  
## 變數filename
> 請輸入影片的絕對路徑，
> 若只有影片名稱.副檔名，則預設為執行目錄底下。  
  
## 可選參數output_location
> 請輸入輸出的資料夾路徑，不用+檔名，  
> 如果不輸入則預設為__root/file/generator底下。  
  
## 可選參數ifMain
> 控制log要不要顯示---Strat func()---,---End func()---  
> 預設為True  
   
## 可選參數ifLog
> 控制要不要把python-ffmpeg執行過程轉換成ffmpeg的cmd指令顯示在log，複寫ifMain  
> 預設為False   
  
## 可選參數ifStdout  
> 控制要不要顯示ffmpeg的stdout訊息，否則只顯示error訊息，預設為False  
> 預設為False  
  
## video_algorithm（位於alalyzer/algorithm）
> 
> ### get_video_length(filename)   
> > 說明：傳入影片，得到影片長度。
> ### get_video_fps(filename)   
> > 說明：傳入影片，得到影片fps。  
  
___    
## video_split（位於generator）
> ### split_by_frame(filename, start_time, frame_number, output_location="")   
> > 說明：從影片的特定時間點切出一張一張的frame  
> > filename: 影片路徑  
> > start_time: 切割開始的時間點  
> > frame_number: 要切的frame張數  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator   
> > bitrate: 影片位元速率，越大圖片畫質越好，檔案容量也越大，預設為5000k  
> > frames的輸出: 會在output_location產生一個[filename的檔案名稱]+_frames的資料夾，並存放切出的frames，如果有存在相同資料夾，則會自動在後面加上_1,_2,...，frames會以影片名稱-編號.jpg命名。  
> ### split_by_manifest(filename, split_start, split_length, output_location="", output_name="", bitrate="5000k")  
> > 說明： 依照自訂義時間切割影片  
> > filename: 影片路徑  
> > split_start: 切割開始的時間點  
> > split_length: 要切割的時間長度  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator  
> > output_name: output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則參照輸入檔案  
> > bitrate: 影片位元速率，越大畫質越好，檔案容量也越大，預設為5000k  
  
___      
## video_contact（位於generator）  
> ### contact_by_type(video_type, input_location="", output_location="", output_name="")  
> > 說明: 把路徑底下，所有同類型的影片合併  
> > video_type: 要合併的影片類型  
> > input_location: 要合併影片的路徑  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator  
> > output_name: [影片名稱].[副檔名]，預設為contact_output_+時戳，副檔名則參照video_type  
> ### contact_by_manifest(video_tuple, output_location="", output_name="output")  
> > 說明：把路徑底下，所有同類型的影片合併  
> > video_type: 要合併的影片類型  
> > input_location: 要合併影片的路徑  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator  
> > output_name: [影片名稱].[副檔名]，預設為contact_output_+時戳，副檔名則參照video_type  
  
___    
## video_process（位於generator）  
> ### video_process(filename, split_list, temp_Keep=False, output_location="", output_name="")  
> > 說明：影片的裁切與合併  
> > filename: 影片路徑  
> > split_list:[(start_time1, end_time1), (start_time2,end_time2))...]  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator  
> > output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則參照輸入檔案  
> > temp_Keep: 處理時會在output_location產生[filename的檔案名稱]+_process_temp的資料夾，可選擇是否保留，如果有存在相同資料夾，則會自動在後面加上_1,_2,...  
> ### video_encoding(filename, output_location="", output_name="", bitrate="5000k")  
> > 說明：影片的轉檔，根據ouput_name的副檔名做重新編碼  
> > filename: 影片路徑  
> > output_location: 輸出位置(不包含檔案)，預設為__root/file/generator  
> > output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則預設為mp4  
> > bitrate: 影片位元速率，越大畫質越好，檔案容量也越大，預設為5000k  