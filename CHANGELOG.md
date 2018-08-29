# Changelog
此專案內所有值得被紀錄的更動都應該被紀錄於此文件。

格式基於 [Keep a Changelog](http://keepachangelog.com/zh-TW/1.0.0/)
這個項目堅持 [Semantic Versioning](http://semver.org/spec/v2.0.0.html)

## [0.0.10]
### Added
- 新增 `crawler/bilibili` 4項標準輸出格式， `comment_crawler`仍未實作

### Fixed
- 修正 `.gitignore` crawler 輸出位置
- 修正 `crawler/bilibili` 輸出位置

## [0.0.9] - 2018-08-24
## Added
- 完善 `README.md` 的系統基礎架構

## [0.0.8] - 2018-08-23
### Added
- 新增 `requirements.txt` 在根目錄

## [0.0.7] - 2018-08-23
### Fixed
- 更改專案結構
- 合併 `bilibili_comment_content_api.py` , `bilibili_info.py` 至 `crawler/bilibili.py` 
- 修正 `bilibili.py` 中 `Bilibili_file_info` load

## [0.0.6] - 2018-08-22
### Fixed
- 修正 logger file hanlder 的編碼問題

## [0.0.5] - 2018-08-18
### Added
- 新增 `helper/use_me.py` 可執行cmd功能
- 新增 bilibili 更多測試

### Fixed
- 修正 helper floder 修正成 package
- 修正非 cmd print 資料換到 log

## [0.0.4] - 2018-08-17
### Added
- .gitignore 增加路徑 envs/, credentials/, .pytest_cache/
- 新增 tools package
- 在 tools package下加入 subpackage: `analyzer`, `bilibili` 的 package 合併自前專案
- 新增 tests/bilibili 資料夾
- 新增 `bilibili_comment_content_apt_test.py`

## [0.0.3] - 2018-08-16
### Fixed
- 修正 log file 不會顯示 __name__ 和 levelname 的問題

## [0.0.2] - 2018-08-10
### Added
- 新增 helper 資料夾
- 在 helper 下新增 logger 模組及新增 logger 資料夾
### Fixed
- logger 資料夾修正成 log

## [0.0.1] - 2018-08-05
### Added
- 新增此更動紀錄檔案。

## [0.0.0] - 2018-08-03
### Added
- 建立此專案並命名為「VeXtract」。