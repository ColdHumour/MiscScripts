# -*- coding: utf-8 -*-

"""
modify_wind_login_info.py

解决 wind 每次登录的字符串显示

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2020.02.25
"""

import os


def modify_wind_login_info():
    info = os.popen("reg query \"HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\万得信息技术有限公司\Wind金融终端\"").read()
    windpath = [line.split("  ")[-1] for line in info.split("\n")
                if line.strip().startswith("Path")][0]
    windpy = os.path.join(windpath, "x64", "WindPy.py")
    assert os.path.exists(windpy)

    with open(windpy, 'r') as file:
        data = file.readlines()
        
    for i, line in enumerate(data):
        if 'print("Welcome' in line:
            if not line.strip().startswith("#"):
                for j in range(i, i+4):
                    data[j] = data[j].replace("print", "# print")
            break

    with open(windpy, 'w') as file:
        file.writelines(data)

    print("Wind login info is modified successfully!")

if __name__ == "__main__":
    modify_wind_login_info()
