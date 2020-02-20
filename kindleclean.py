# -*- coding: utf-8 -*-

"""
kindle_clean.py

清除不必要的书签文件夹

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2020.02.20
"""

import os
import psutil
import shutil
import subprocess


def kindle_clean(kindlefolder):
    errflag = 1
    for disk in  psutil.disk_partitions():
        volinfo = subprocess.check_output(["cmd", "/c vol {}".format(disk.device.strip("\\"))])
        try:
            volinfo = volinfo.decode("utf-8")
        except UnicodeDecodeError:
            volinfo = volinfo.decode("gbk")
        finally:
            label = volinfo.split("\r\n")[0].split(" ").pop()

        if label == "kindle":
            errflag = 0
            break

    if errflag:
        raise ValueError("Kindle disk not found!")

    kindlefolder = os.path.join(label, "documents")
    files = os.listdir(kindlefolder)
    ebooks = [f for f in files if f.split(".").pop() in "pdf|azw3|mobi"]
    sdrfolders = [f for f in files if f.endswith("sdr")]
