# Youtube Crawler

## 檔案說明

### `youtube_info.py`

可以抓取以下資訊:  
`標題` `作者` `編號` `長度` `評分 (按讚的比例/全部的比例*5)` `閱覽數` `縮圖`

使用方式:
目前僅供程式呼叫
```
from youtube_info import get_video_by_url
video = get_video_by_url(url)
```
Output: video.title <- 會顯示標題  
Output: video.getbest().url <- 會顯示可下載的 url  

未來開發:
1. 可以直接執行的介面
2. 串流的下載方式

### `youtube_comment.py`

可以抓取以下資訊:  
`留言者id(cid)` `留言者(author)` `留言文字(txt)` `留言時間(time) p.s XX 天前`

使用方式:
`python youtube_comment.py -y 影片id -o 輸出位置.json`

未來開發:
1. 更人性化的使用介面