
## ffmepg環境設定
> 1.先到這個網頁 https://jsnwork.kiiuo.com/archives/2705/ffmpeg-windows-%E5%AE%89%E8%A3%9D/  
> 2.照上面的說明安裝ffmpeg，並設定環境變數  
> 3.檔案若非在執行的根目錄底下，就要輸入檔案的完整路徑（路徑不要加"" or ''）

# 主要功能說明

## 變數filename
>
 請輸入影片的絕對路徑，
 若只有影片名稱.副檔名，則預設為執行目錄底下。

## 輸出檔案
>
 輸出檔案都會被自動放到file資料夾裡。

## video_algorithm（位於alalyzer/algorithm）
>
 get_video_length(filename) 說明：傳入影片，得到影片長度。
 get_video_fps(filename) 說明：傳入影片，得到影片fps。

## video_split（位於generator）
>
 split_by_frame(filename, start_time, frame_number)   
 說明：對影片切出一張一張的frame，start_time為切割開始的時間（以秒數輸入），frame_number為要切割的張數，  
       輸出會產生一個temp資料夾，圖片會以影片名稱-編號.jpg命名。  
 --------------------------------------------------------------------------------------------------         
 split_by_manifest(filename, split_start, split_length, rename_to, cmd_extra_code="", ifmove=True)   
 說明：對影片進行自定義切割，split_start為切割開始的時間（以秒數輸入），split_length為切割的長度，  
        rename_to為輸出檔案的命名（須加附檔名），cmd_extra_code為在切割前進行的額外cmd指令，不用理會，  
        ifmove代表要不要移動切割後的影片到file資料夾裡。  

## video_contact（位於generator）
>
 contact_by_manifest(video_tuple, output_type, output_name="output")  
 說明：傳入一個video_tuple（複數的個filename），並合併成一個影片，  
        output_name則是輸出的影片名稱，可輸入路徑或影片名稱.副檔名，若不輸入則預設為"output"。  

## video_process（位於generator）
>
 video_process(filename, split_list, temp_Keep=False, output_name="output")  
 說明：傳入影片，並且傳入複數切割的時間點split_list（格式為 [(開始的秒數,要切割的長度),(開始的秒數,要切割的長度),....]），  
        最後合併成一個影片，temp_keep為切割過程產生的分割檔是否要保留（預設為false），output_name則是輸出的影片名稱，  
        若不輸入則預設為"output"。  