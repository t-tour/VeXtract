import argparse
import traceback
import os
import sys
sys.path.append(os.path.dirname(__file__))


from bilibili.bilibili.bilibili_comment_content_api import get_comment_data  # noqa
from analyzer import text_sentiment_analyze as text_sent

DEFAULT_DIR = ''


def main():
    parser = argparse.ArgumentParser(
        description="用於獲取bilibili站一般視頻或裡面的彈幕")
    parser.add_argument('-a', '--avnumbers', nargs='*',
                        help="下載AV號 -a av123456 av...")
    parser.add_argument('-o', '--output', help="輸出位置", default="chat_xml_res/")
    parser.add_argument('-v', '--video', help="是否下載視頻", action="store_true")
    parser.add_argument('-d', '--danmaku', help="是否下載彈幕", action="store_true")
    parser.add_argument('-s', '--score', help="是否評分", action="store_true")
    # TODO: 加入可以從檔案讀取avnumber
    # 像是csv檔案用\t切開的文字檔
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    args = parser.parse_args()

    if args.avnumbers is not None:
        print(str.format("下載xml至{0}:", os.path.abspath(args.output)))
        for av in args.avnumbers:
            try:
                get_comment_data(av, args.output)
                print(str.format("\t{0} 下載完成", av))

            except FileExistsError:
                os.chdir("../")
                print(str.format("\t{0} 檔案已存在", av))
            except Exception as e:
                print(str.format("\t{0} 錯誤:{1}", av, e.args[0]))


if __name__ == "__main__":
    main()
