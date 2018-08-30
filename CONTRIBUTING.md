# 協作

當功能確認開發完成後，可以不撰寫測試即可 merge 到 master。但需要開 pull request。
未來會改成必須寫 test 才算完成。

## Pull Request 程序

1. 確認你使用到的 library 有被你加到 requirements.txt 中。
2. 你的 commit 應該要符合 [Git風格指南](https://github.com/JuanitoFatas/git-style-guide)
3. 發送 Pull Request 時應該要把重大的新增(Added)、修復(Fixed)及改變(Changed)，
   還有 一些想要打在 README.md 中的資訊，打在 Pull Request 描述中。

## Pull Request 審核

1. 確認開發者有符合以上三點。
2. 測試此 branch 的功能是否能夠正常運行。
3. merge 後修改 REAMDE.md 和 CHANGELOG.md
   注意版本號要根據 [語意化版本號](https://semver.org/lang/zh-TW/)。

## 開發指南

* 待補充