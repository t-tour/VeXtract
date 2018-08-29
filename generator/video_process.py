import video_contact
import video_split
import subprocess
import re
import math
import os
from optparse import OptionParser


def video_process(filename,split_list):
    count=0
    video_name= filename.split(".")[0]
    video_type = filename.split(".")[1]
    subprocess.Popen("md temp", shell=True,stdout=subprocess.PIPE).stdout.read()
    for i in split_list:
        split_start= int(i[0])
        split_length = int(i[1])-split_start
        rename_to = video_name +"-"+str(count)+"."+video_type
        count = count+1
        video_split.split_by_manifest(os.path.join(os.getcwd(),filename),split_start,split_length,rename_to)

    video_contact.contact_by_type(video_type,video_type)

if __name__ == "__main__":
    #測試用
    split_list=[(1,3),(6,10),(15,30)]#傳入的list of tuple
    video_process("01.mp4",split_list)#(檔案名稱,list of tuple)   

