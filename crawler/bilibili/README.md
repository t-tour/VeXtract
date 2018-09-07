## `bilibili.py`
> 一般使用請 import 這個檔案  
有疑問可以參考 `bilibili_info.py` 裡面的 `bilibili_file_info` 這個 class
### 使用例
```
from crawler.bilibili import bilibili

url = "https://www.bilibili.com/video/av5275610"
```
#### info_crawler
```
a = bilibili.info_crawler(url)
print(a)
```
#### real_time_comment_crawler
```
b = bilibili.real_time_comment_crawler(url)
print(b)
```
#### file_crawler
```
bilibili.file_crawler(url)
```