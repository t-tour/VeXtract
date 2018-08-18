import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (len(os.path.dirname(os.path.abspath(__file__)).split(os.sep)) -
                                                                                os.path.dirname(os.path.abspath(__file__)).split(os.sep).index('VeXtract') - 1))
import argparse
import traceback


from tools.bilibili import bilibili_comment_content_api as bci  # noqa
from tools.analyzer import text_sentiment_analyze as text_sent

DEFAULT_DIR = ''


def main():
    parser = argparse.ArgumentParser(
        description="用於獲取bilibili站一般視頻或裡面的彈幕")
    parser.add_argument('-a', '--avnumbers', nargs='*',
                        help="下載AV號 -a av123456 av...")
    parser.add_argument('-o', '--output', help="輸出位置", default="/json")
    parser.add_argument('-v', '--video', help="是否下載視頻", action="store_true")
    parser.add_argument('-s', '--score', help="是否評分", action="store_true")
    parser.add_argument('-l', '--limitation', help="評分上限數量", default=100, type=int)
    parser.add_argument('-sf', '--score_false',
                        help="評分但不上GCP", action="store_false")
    # TODO: 加入可以從檔案讀取avnumber
    # 像是csv檔案用\t切開的文字檔
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    args = parser.parse_args()

    if args.avnumbers is not None:
        print(str.format("下載至{0}:", os.path.abspath(
            os.getcwd() + args.output)))
        for av in args.avnumbers:
            try:
                dow = bci.fetch_bilibili_av(av)
                if args.score:
                    dow.fetch_comment_score(
                        limitation=args.limitation)
                dow.save()
                if args.video:
                    bci.get_video_data("av{}".format(dow.aid))
                print(str.format("\t{0} 下載完成", av))
            except FileExistsError:
                os.chdir("../")
                print(str.format("\t{0} 檔案已存在", av))
#            except Exception as e:
#                print(str.format("\t{0} 錯誤:{1}", av, e.args[0]))


if __name__ == "__main__":
    main()
